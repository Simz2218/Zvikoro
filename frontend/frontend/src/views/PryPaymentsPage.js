// ...imports stay the same
import React, { useEffect, useState, useContext } from "react";
import useAxios from "../utils/useAxios";
import backgroundImage from "./pictures/great_zimbabwe.jpg";
import Swal from "sweetalert2";
import AuthContext from "../context/AuthContext";
import * as XLSX from "xlsx";
import jsPDF from "jspdf";


import autoTable from "jspdf-autotable";



function PaymentsPage() {
  const { axiosInstance } = useAxios();
  const { updateTermBalances } = useContext(AuthContext);

  // UI state
  const [paymentType, setPaymentType] = useState("primary"); // "primary" | "secondary"
  const [submitting, setSubmitting] = useState(false);

  // Data
  const [schools, setSchools] = useState([]);
  const [payments, setPayments] = useState([]);

  // Filters
  const [filterSchool, setFilterSchool] = useState("");
  const [filterYear, setFilterYear] = useState("");
  const [filterTerm, setFilterTerm] = useState("");

  // Editing
  const [editingRowId, setEditingRowId] = useState(null);
  const [editForm, setEditForm] = useState({ paid_amount: "", date_paid: "" });

  // Endpoints by type
  const schoolEndpoint =
    paymentType === "primary" ? "primary-schools/" : "secondary-schools/";
  const paymentsEndpoint =
    paymentType === "primary" ? "pry-payments/" : "sec-payments/";

  // Helpers: date conversions
  const intToDateInput = (intYmd) => {
    if (!intYmd) return "";
    const s = String(intYmd);
    if (s.length !== 8) return "";
    return `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`;
  };
  const dateInputToInt = (yyyy_mm_dd) =>
    parseInt(String(yyyy_mm_dd || "").replaceAll("-", ""), 10);

  // Load schools when type changes
  useEffect(() => {
    const loadSchools = async () => {
      try {
        const res = await axiosInstance.get(schoolEndpoint);
        if (res.status === 200) {
          setSchools(res.data || []);
        } else {
          Swal.fire("Error", "Failed to load school list", "error");
        }
      } catch (err) {
        console.error(err);
        Swal.fire("Error", "Could not load schools", "error");
      }
    };
    loadSchools();
  }, [axiosInstance, schoolEndpoint]);

  // Load payments
  const loadPayments = async () => {
    try {
      const res = await axiosInstance.get(paymentsEndpoint);
      if (res.status === 200) {
        setPayments(res.data || []);
      }
    } catch (err) {
      console.error(err);
      Swal.fire("Error", "Could not load payments", "error");
    }
  };

  // Load payments on mount & when type changes
  useEffect(() => {
    setEditingRowId(null); // reset edit mode when switching
    loadPayments();
  }, [paymentType]); // eslint-disable-line react-hooks/exhaustive-deps

  // Update balances (server-side) then refresh
  const handleUpdateBalances = async () => {
    const ok = await updateTermBalances();
    if (ok) {
      await loadPayments();
      Swal.fire("Updated", "Term balances refreshed.", "success");
    }
  };

  // Start editing
  const startEditing = (row) => {
    setEditingRowId(row.id);
    setEditForm({
      paid_amount: String(row.paid_amount ?? ""),
      // Convert backend int yyyymmdd -> input yyyy-mm-dd for the date input
      date_paid: intToDateInput(row.date_paid),
    });
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingRowId(null);
    setEditForm({ paid_amount: "", date_paid: "" });
  };

  // Save edited row
  const saveEdit = async (id) => {
    const payload = {
      paid_amount: parseInt(editForm.paid_amount, 10),
      // Convert input yyyy-mm-dd -> backend int yyyymmdd
      date_paid: dateInputToInt(editForm.date_paid),
    };

    if (
      isNaN(payload.paid_amount) ||
      !payload.date_paid ||
      String(payload.date_paid).length !== 8
    ) {
      Swal.fire("Error", "Please enter a valid amount and date.", "error");
      return;
    }

    try {
      await axiosInstance.put(`${paymentsEndpoint}${id}/`, payload);
      Swal.fire("Success", "Payment updated", "success");
      setEditingRowId(null);
      await loadPayments();
    } catch (err) {
      console.error(err);
      let msg = "Failed to save changes.";
      if (err.response?.data) {
        msg = Object.values(err.response.data).join("\n");
      }
      Swal.fire("Error", msg, "error");
    }
  };

  // Add new payment
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    const school = parseInt(e.target.school.value, 10);
    const paid_amount = parseInt(e.target.paid_amount.value, 10);
    const date_paid_str = e.target.date_paid.value;

    if (!school || isNaN(paid_amount) || !date_paid_str) {
      Swal.fire("Error", "Please fill in all fields correctly.", "error");
      setSubmitting(false);
      return;
    }

    const date_paid = dateInputToInt(date_paid_str);

    try {
      const res = await axiosInstance.post(paymentsEndpoint, {
        school,
        paid_amount,
        date_paid,
      });

      if (res.status === 201) {
        Swal.fire("Success", "Payment recorded successfully.", "success");
        e.target.reset();
        await loadPayments();
      } else {
        Swal.fire("Error", "Unexpected server response.", "error");
      }
    } catch (err) {
      console.error(err);
      let msg = "Failed to save payment.";
      if (err.response?.data) {
        msg = Object.values(err.response.data).join("\n");
      }
      Swal.fire("Error", msg, "error");
    } finally {
      setSubmitting(false);
    }
  };

  // Filtering
  const filteredPayments = payments.filter((p) => {
    const schoolMatch = (p.school_name || "")
      .toLowerCase()
      .includes(filterSchool.toLowerCase());
    const yearMatch = filterYear ? p.year === parseInt(filterYear, 10) : true;
    const termMatch = filterTerm ? p.term === parseInt(filterTerm, 10) : true;
    return schoolMatch && yearMatch && termMatch;
  });

  // Options (derive from dataset to keep it simple)
  const years = Array.from(new Set(payments.map((p) => p.year))).sort(
    (a, b) => b - a
  );
  const terms = Array.from(new Set(payments.map((p) => p.term))).sort(
    (a, b) => a - b
  );

  // Export: Excel
  const exportExcel = () => {
    const rows = filteredPayments.map((p) => ({
      School: p.school_name,
      Year: p.year,
      Term: p.term,
      Amount: p.paid_amount,
      DatePaid: intToDateInput(p.date_paid),
      Balance: p.balance,
    }));
    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Payments");
    XLSX.writeFile(wb, `${paymentType}_payments.xlsx`);
  };

  const exportPDF = () => {
    const doc = new jsPDF();
    autoTable(doc, {
      head: [["School", "Year", "Term", "Amount", "Date Paid", "Balance"]],
      body: filteredPayments.map((p) => [
        p.school_name,
        p.year,
        p.term,
        p.paid_amount,
        intToDateInput(p.date_paid),
        p.balance,
      ]),
    });
    doc.save(`${paymentType}_payments.pdf`);
  };
  return (
    <div
      className="min-vh-100 d-flex align-items-center justify-content-center"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="container bg-white p-4 rounded shadow-lg">
        <h2 className="text-center text-primary mb-4">
          {paymentType === "primary" ? "Primary" : "Secondary"} Schools Payments
        </h2>

        {/* Toggle */}
        <div className="mb-3">
          <button
            className={`btn me-2 ${
              paymentType === "primary" ? "btn-primary" : "btn-outline-primary"
            }`}
            onClick={() => setPaymentType("primary")}
          >
            Primary
          </button>
          <button
            className={`btn ${
              paymentType === "secondary" ? "btn-primary" : "btn-outline-primary"
            }`}
            onClick={() => setPaymentType("secondary")}
          >
            Secondary
          </button>
        </div>

        {/* Filters + balances */}
        <div className="d-flex flex-wrap gap-2 mb-3">
          <input
            type="text"
            className="form-control"
            style={{ minWidth: 220, flex: "1 1 240px" }}
            placeholder="Filter by school..."
            value={filterSchool}
            onChange={(e) => setFilterSchool(e.target.value)}
          />
          <select
            className="form-select"
            style={{ width: 140 }}
            value={filterYear}
            onChange={(e) => setFilterYear(e.target.value)}
          >
            <option value="">All Years</option>
            {years.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
          <select
            className="form-select"
            style={{ width: 130 }}
            value={filterTerm}
            onChange={(e) => setFilterTerm(e.target.value)}
          >
            <option value="">All Terms</option>
            {terms.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <button className="btn btn-warning ms-auto" onClick={handleUpdateBalances}>
            Update Term Balances
          </button>
        </div>

        {/* Export */}
        <div className="mb-3">
          <button className="btn btn-success me-2" onClick={exportExcel}>
            Export Excel
          </button>
          <button className="btn btn-danger" onClick={exportPDF}>
            Export PDF
          </button>
        </div>

        {/* Payments table */}
        <div className="table-responsive">
          <table className="table table-bordered align-middle">
            <thead>
              <tr>
                <th>School</th>
                <th>Year</th>
                <th>Term</th>
                <th>Amount</th>
                <th>Date Paid</th>
                <th>Balance</th>
                <th style={{ width: 140 }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredPayments.map((p) => (
                <tr key={`${paymentType}-${p.id}`}>
                  <td>{p.school_name}</td>
                  <td>{p.year}</td>
                  <td>{p.term}</td>
                  <td style={{ maxWidth: 140 }}>
                    {editingRowId === p.id ? (
                      <input
                        type="number"
                        min="0"
                        className="form-control form-control-sm"
                        value={editForm.paid_amount}
                        onChange={(e) =>
                          setEditForm({
                            ...editForm,
                            paid_amount: e.target.value,
                          })
                        }
                      />
                    ) : (
                      p.paid_amount
                    )}
                  </td>
                  <td style={{ maxWidth: 170 }}>
                    {editingRowId === p.id ? (
                      <input
                        type="date"
                        className="form-control form-control-sm"
                        value={editForm.date_paid}
                        onChange={(e) =>
                          setEditForm({
                            ...editForm,
                            date_paid: e.target.value,
                          })
                        }
                      />
                    ) : (
                      intToDateInput(p.date_paid) || p.date_paid
                    )}
                  </td>
                  <td>{p.balance}</td>
                  <td>
                    {editingRowId === p.id ? (
                      <div className="d-flex gap-2">
                        <button
                          className="btn btn-success btn-sm"
                          onClick={() => saveEdit(p.id)}
                        >
                          Save
                        </button>
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={cancelEditing}
                        >
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <button
                        className="btn btn-primary btn-sm"
                        onClick={() => startEditing(p)}
                      >
                        Edit
                      </button>
                    )}
                  </td>
                </tr>
              ))}
              {filteredPayments.length === 0 && (
                <tr>
                  <td colSpan="7" className="text-center text-muted">
                    No payments match the current filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Add new payment form */}
        <form onSubmit={handleSubmit} className="mt-4">
          <div className="row g-3">
            <div className="col-md-5">
              <label className="form-label">School</label>
              <select name="school" className="form-select" required>
                <option value="">-- Select a School --</option>
                {schools.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name}
                    {s.district ? ` (${s.district})` : ""}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-3">
              <label className="form-label">Amount</label>
              <input
                name="paid_amount"
                type="number"
                min="0"
                className="form-control"
                required
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">Date Paid</label>
              <input name="date_paid" type="date" className="form-control" required />
            </div>
          </div>
          <button className="btn btn-primary w-100 mt-3" disabled={submitting}>
            {submitting ? "Submitting..." : "Submit Payment"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default PaymentsPage;
