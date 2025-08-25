import React, { useEffect, useState, useContext } from "react";
import useAxios from "../utils/useAxios";
import backgroundImage from "./pictures/great_zimbabwe.jpg";
import Swal from "sweetalert2";
import AuthContext from "../context/AuthContext";

function SecPaymentsPage() {
  const { axiosInstance } = useAxios();
  const { updateTermBalances } = useContext(AuthContext);

  const [submitting, setSubmitting] = useState(false);
  const [schools, setSchools] = useState([]);
  const [payments, setPayments] = useState([]);
  const [filter, setFilter] = useState("");
  const [editingRowId, setEditingRowId] = useState(null);
  const [editForm, setEditForm] = useState({ paid_amount: "", date_paid: "" });

  // Load school list
  useEffect(() => {
    const loadSchools = async () => {
      try {
        const res = await axiosInstance.get("secondary-schools/");
        if (res.status === 200) {
          setSchools(res.data);
        } else {
          Swal.fire("Error", "Failed to load school list", "error");
        }
      } catch (err) {
        console.error(err);
        Swal.fire("Error", "Could not load schools", "error");
      }
    };
    loadSchools();
  }, [axiosInstance]);

  // Load payments
  const loadPayments = async () => {
    try {
      const res = await axiosInstance.get("sec-payments/");
      if (res.status === 200) {
        setPayments(res.data);
      }
    } catch (err) {
      console.error(err);
      Swal.fire("Error", "Could not load payments", "error");
    }
  };

  useEffect(() => {
    loadPayments();
  }, []);

  // Update balances via AuthContext
  const handleUpdateBalances = async () => {
    const ok = await updateTermBalances();
    if (ok) {
      loadPayments();
    }
  };

  // Editing helpers
  const startEditing = (row) => {
    setEditingRowId(row.id);
    setEditForm({ paid_amount: row.paid_amount, date_paid: row.date_paid });
  };

  const saveEdit = async (id) => {
    try {
      await axiosInstance.put(`sec-payments/${id}/`, editForm);
      Swal.fire("Success", "Payment updated", "success");
      setEditingRowId(null);
      loadPayments();
    } catch (err) {
      Swal.fire("Error", "Failed to save changes", "error");
    }
  };

  // Payment form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    const school_name = e.target.school_name.value;
    const paid_amount = parseInt(e.target.paid_amount.value, 10);
    const date_paid_str = e.target.date_paid.value;

    if (!school_name || isNaN(paid_amount) || !date_paid_str) {
      Swal.fire("Error", "Please fill in all fields correctly.", "error");
      setSubmitting(false);
      return;
    }

    const date_paid = parseInt(date_paid_str.replaceAll("-", ""), 10);

    try {
      const res = await axiosInstance.post("sec-payments/", {
        school_name,
        paid_amount,
        date_paid,
      });

      if (res.status === 201) {
        Swal.fire(
          "Success",
          "Secondary payment recorded successfully.",
          "success"
        );
        e.target.reset();
        loadPayments();
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

  const filteredPayments = payments.filter((p) =>
    p.school_name.toLowerCase().includes(filter.toLowerCase())
  );

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
          Secondary Schools Payments
        </h2>

        {/* Filter + Update button */}
        <div className="d-flex justify-content-between align-items-center mb-3">
          <input
            type="text"
            className="form-control w-50"
            placeholder="Filter by school..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
          <button className="btn btn-warning" onClick={handleUpdateBalances}>
            Update Term Balances
          </button>
        </div>

        {/* Payments table */}
        <table className="table table-bordered">
          <thead>
            <tr>
              <th>School</th>
              <th>Amount</th>
              <th>Date Paid</th>
              <th>Balance</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredPayments.map((p) => (
              <tr key={p.id}>
                <td>{p.school_name}</td>
                <td>
                  {editingRowId === p.id ? (
                    <input
                      type="number"
                      value={editForm.paid_amount}
                      onChange={(e) =>
                        setEditForm({ ...editForm, paid_amount: e.target.value })
                      }
                    />
                  ) : (
                    p.paid_amount
                  )}
                </td>
                <td>
                  {editingRowId === p.id ? (
                    <input
                      type="date"
                      value={editForm.date_paid}
                      onChange={(e) =>
                        setEditForm({ ...editForm, date_paid: e.target.value })
                      }
                    />
                  ) : (
                    p.date_paid
                  )}
                </td>
                <td>{p.balance}</td>
                <td>
                  {editingRowId === p.id ? (
                    <button
                      className="btn btn-success btn-sm"
                      onClick={() => saveEdit(p.id)}
                    >
                      Save
                    </button>
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
          </tbody>
        </table>

        {/* Add new payment form */}
        <form onSubmit={handleSubmit} className="mt-4">
          <div className="mb-3">
            <label className="form-label">School Name</label>
            <select name="school_name" className="form-select" required>
              <option value="">-- Select a School --</option>
              {schools.map((school) => (
                <option key={school.id} value={school.name}>
                  {school.name} ({school.district})
                </option>
              ))}
            </select>
          </div>
          <div className="mb-3">
            <label className="form-label">Amount</label>
            <input
              name="paid_amount"
              type="number"
              min="0"
              className="form-control"
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Date Paid</label>
            <input
              name="date_paid"
              type="date"
              className="form-control"
              required
            />
          </div>
          <button className="btn btn-primary w-100" disabled={submitting}>
            {submitting ? "Submitting..." : "Submit Payment"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default SecPaymentsPage;
