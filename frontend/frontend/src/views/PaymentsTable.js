import React, { useEffect, useState } from "react";
import useAxios from "../utils/useAxios";
import backgroundImage from "./pictures/great_zimbabwe.jpg";
import bluesky from "../views/pictures/bluesky.png";

function PaymentsTable() {
  const { axiosInstance } = useAxios();
  const [payments, setPayments] = useState([]);
  const [schools, setSchools] = useState([]);
  const [type, setType] = useState("secondary");
  const [filters, setFilters] = useState({ school: "", year: "", term: "" });

  useEffect(() => {
    loadData();
    loadSchools();
  }, [type]);

  const loadData = async () => {
    try {
      const endpoint = type === "secondary" ? "sec-payments/" : "pry-payments/";
      const res = await axiosInstance.get(endpoint);
      setPayments(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadSchools = async () => {
    try {
      const endpoint =
        type === "secondary" ? "secondary-schools/" : "primary-schools/";
      const res = await axiosInstance.get(endpoint);
      setSchools(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleEdit = async (id, field, value) => {
    setPayments((prev) =>
      prev.map((p) => (p.id === id ? { ...p, [field]: value } : p))
    );
    try {
      const endpoint =
        type === "secondary" ? `sec-payments/${id}/` : `pry-payments/${id}/`;
      await axiosInstance.patch(endpoint, { [field]: value });
    } catch (err) {
      console.error(err);
      alert("Update failed");
      loadData();
    }
  };

  const filteredPayments = payments.filter((p) => {
    return (
      (filters.school ? p.school === filters.school : true) &&
      (filters.year ? String(p.year) === filters.year : true) &&
      (filters.term ? String(p.term) === filters.term : true)
    );
  });

  return (
    <div
      className="min-vh-100 p-4"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="container bg-white p-4 rounded shadow-lg">
        {/* Header & Toggle */}
        <div className="d-flex justify-content-between align-items-center mb-3 flex-wrap">
          <h2 className="text-primary mb-2">
            {type === "secondary"
              ? "Secondary Schools Payments"
              : "Primary Schools Payments"}
          </h2>
          <div className="btn-group">
            <button
              className={`btn ${type === "secondary" ? "btn-primary" : "btn-outline-primary"}`}
              onClick={() => setType("secondary")}
            >
              Secondary
            </button>
            <button
              className={`btn ${type === "primary" ? "btn-primary" : "btn-outline-primary"}`}
              onClick={() => setType("primary")}
            >
              Primary
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="row mb-3">
          <div className="col-md-4">
            <select
              className="form-select"
              value={filters.school}
              onChange={(e) => setFilters({ ...filters, school: e.target.value })}
            >
              <option value="">All Schools</option>
              {schools.map((school) => (
                <option key={school.id} value={school.name}>
                  {school.name} ({school.district})
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-3">
            <input
              type="number"
              className="form-control"
              placeholder="Year"
              value={filters.year}
              onChange={(e) => setFilters({ ...filters, year: e.target.value })}
            />
          </div>
          <div className="col-md-3">
            <input
              type="number"
              className="form-control"
              placeholder="Term"
              value={filters.term}
              onChange={(e) => setFilters({ ...filters, term: e.target.value })}
            />
          </div>
          <div className="col-md-2">
            <button
              className="btn btn-secondary w-100"
              onClick={() => setFilters({ school: "", year: "", term: "" })}
            >
              Reset
            </button>
          </div>
        </div>

        {/* Table */}
        <table className="table table-bordered table-hover table-sm">
          <thead className="table-light">
            <tr>
              <th>School</th>
              <th>Amount</th>
              <th>Date Paid</th>
              <th>Balance</th>
              <th>Year</th>
              <th>Term</th>
            </tr>
          </thead>
          <tbody>
            {filteredPayments.map((pay) => (
              <tr key={pay.id}>
                <td>
                  <select
                    className="form-select"
                    value={pay.school}
                    onChange={(e) => handleEdit(pay.id, "school", e.target.value)}
                  >
                    <option value="">-- Select --</option>
                    {schools.map((school) => (
                      <option key={school.id} value={school.name}>
                        {school.name} ({school.district})
                      </option>
                    ))}
                  </select>
                </td>
                <td>
                  <input
                    type="number"
                    className="form-control"
                    value={pay.paid_amount}
                    onChange={(e) =>
                      handleEdit(pay.id, "paid_amount", parseInt(e.target.value, 10))
                    }
                  />
                </td>
                <td>
                  <input
                    type="date"
                    className="form-control"
                    value={String(pay.date_paid)}
                    onChange={(e) => handleEdit(pay.id, "date_paid", e.target.value)}
                  />
                </td>
                <td>{pay.balance}</td>
                <td>
                  <input
                    type="number"
                    className="form-control"
                    value={pay.year}
                    onChange={(e) =>
                      handleEdit(pay.id, "year", parseInt(e.target.value, 10))
                    }
                  />
                </td>
                <td>
                  <input
                    type="number"
                    className="form-control"
                    value={pay.term}
                    onChange={(e) =>
                      handleEdit(pay.id, "term", parseInt(e.target.value, 10))
                    }
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PaymentsTable;
