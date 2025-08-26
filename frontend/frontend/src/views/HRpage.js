// src/pages/HRpage.js
import React, {
  useEffect,
  useState,
  useContext,
  useMemo
} from "react";
import AuthContext from "../context/AuthContext";
import Swal from "sweetalert2";
import bluesky from "../views/pictures/bluesky.png";
const HRpage = () => {
  const { authFetch, authTokens, URLS } = useContext(AuthContext);

  // State buckets
  const [secSchools, setSecSchools]   = useState([]);
  const [secGrades, setSecGrades]     = useState([]);
  const [secTeachers, setSecTeachers] = useState([]);
  const [priSchools, setPriSchools]   = useState([]);
  const [priGrades, setPriGrades]     = useState([]);
  const [priTeachers, setPriTeachers] = useState([]);

  const [loading, setLoading]     = useState(true);
  const [uploading, setUploading] = useState(false);
  const [filePrimary, setFilePrimary]     = useState(null);
  const [fileSecondary, setFileSecondary] = useState(null);
  const [activeTab, setActiveTab] = useState("secondary");

  // Fetch all 6 endpoints in parallel
  const fetchData = async () => {
    setLoading(true);
    try {
      const [
        schoolsSec, gradesSec, teachersSec,
        schoolsPri, gradesPri, teachersPri
      ] = await Promise.all([
        authFetch(URLS.sSchools).then(r => r.json()),
        authFetch(URLS.sGradeEnrollments).then(r => r.json()),
        authFetch(URLS.sTeacherData).then(r => r.json()),
        authFetch(URLS.pSchools).then(r => r.json()),
        authFetch(URLS.gradeEnrollments).then(r => r.json()),
        authFetch(URLS.teacherData).then(r => r.json())
      ]);

      setSecSchools(schoolsSec);
      setSecGrades(gradesSec);
      setSecTeachers(teachersSec);
      setPriSchools(schoolsPri);
      setPriGrades(gradesPri);
      setPriTeachers(teachersPri);
    } catch (error) {
      console.error(error);
      Swal.fire("Error", "Failed to load HR data", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line
  }, []);

  // Helpers to group and sum
  const groupBySchool = rows => {
    const map = new Map();
    rows.forEach(r => {
      const arr = map.get(r.school) || [];
      arr.push(r);
      map.set(r.school, arr);
    });
    return map;
  };

  const secGradesBySchool = useMemo(() => groupBySchool(secGrades), [secGrades]);
  const secTeachersBySchool = useMemo(() => groupBySchool(secTeachers), [secTeachers]);
  const priGradesBySchool = useMemo(() => groupBySchool(priGrades), [priGrades]);
  const priTeachersBySchool = useMemo(() => groupBySchool(priTeachers), [priTeachers]);

  const sumField = (rows, field) =>
    rows.reduce((sum, r) => sum + (Number(r[field]) || 0), 0);

  const renderGradesCell = rows => {
    if (!rows.length) return <span className="text-muted">—</span>;
    return (
      <div>
        {rows.map(g => (
          <div key={g.id}>
            <strong>{g.level}:</strong>{" "}
            M {g.male||0}, F {g.female||0}, T {g.total||0} (Y{g.year})
          </div>
        ))}
        <hr className="my-2" />
        <div className="fw-semibold">
          Total: M {sumField(rows, "male")}, F {sumField(rows, "female")}, T {sumField(rows, "total")}
        </div>
      </div>
    );
  };

  const renderTeachersCell = rows => {
    if (!rows.length) return <span className="text-muted">—</span>;
    return (
      <div>
        {rows.map(t => (
          <div key={t.id}>
            <strong>{t.level}:</strong>{" "}
            M {t.male||0}, F {t.female||0}, T {t.total||0},{" "}
            AE {t.authorized_establishment||0}, Vac {t.vacancies||0} (Y{t.year})
          </div>
        ))}
        <hr className="my-2" />
        <div className="fw-semibold">
          Total: M {sumField(rows, "male")}, F {sumField(rows, "female")}, T {sumField(rows, "total")},{" "}
          AE {sumField(rows, "authorized_establishment")}, Vac {sumField(rows, "vacancies")}
        </div>
      </div>
    );
  };

  // Upload via authFetch so token refresh works
  const handleUpload = async which => {
    const file = which === "primary" ? filePrimary : fileSecondary;
    const url  = which === "primary" ? URLS.uploadExcel : URLS.sUploadExcel;

    if (!file) {
      return Swal.fire("Select a file", "Please choose an Excel file.", "info");
    }

    const form = new FormData();
    form.append("file", file);

    setUploading(true);
    try {
      const res = await authFetch(url, {
        method: "POST",
        body: form
        // authFetch omits Content-Type for FormData automatically
      });
      if (!res.ok) throw new Error("Upload failed");
      Swal.fire("Uploaded", "Excel uploaded successfully.", "success");
      await fetchData();
    } catch (err) {
      console.error(err);
      Swal.fire("Error", "Excel upload failed.", "error");
    } finally {
      setUploading(false);
      which === "primary" ? setFilePrimary(null) : setFileSecondary(null);
    }
  };

  // Client-side CSV export of schools + basic fields
  const handleExport = () => {
    const schools = activeTab === "secondary" ? secSchools : priSchools;
    if (!schools.length) {
      return Swal.fire("No data", "Nothing to export.", "info");
    }

    const header = ["School", "District", "Status", "Year"];
    const rows = schools.map(s => [
      s.name,
      s.district,
      s.registration_status,
      s.year
    ]);

    const csvLines = [header, ...rows]
      .map(r => r.map(cell => `"${cell}"`).join(","))
      .join("\n");

    const blob = new Blob([csvLines], { type: "text/csv" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${activeTab}-schools.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return <div className="container mt-4">Loading data…</div>;
  }

  const rows = activeTab === "secondary" ? secSchools : priSchools;

  return (
    <div className="container mt-4">
      <h2>HR Dashboard</h2>

      <div className="btn-group mb-4">
        <button
          className={`btn ${activeTab === "secondary" ? "btn-primary" : "btn-outline-primary"}`}
          onClick={() => setActiveTab("secondary")}
        >
          Secondary
        </button>
        <button
          className={`btn ${activeTab === "primary" ? "btn-primary" : "btn-outline-primary"}`}
          onClick={() => setActiveTab("primary")}
        >
          Primary
        </button>
      </div>

      <div className="card">
        <div className="card-header d-flex flex-wrap gap-2 justify-content-between align-items-center">
          <h5 className="mb-0">
            {activeTab === "secondary"
              ? "Secondary Schools Data"
              : "Primary Schools Data"}
          </h5>

          <div className="d-flex gap-2">
            {/* Export CSV */}
            <button
              className="btn btn-outline-success"
              onClick={handleExport}
            >
              Export CSV
            </button>

            {/* Upload Excel */}
            <div className="input-group" style={{ maxWidth: 280 }}>
              <input
                type="file"
                accept=".xls,.xlsx"
                className="form-control"
                onChange={e =>
                  activeTab === "primary"
                    ? setFilePrimary(e.target.files[0] || null)
                    : setFileSecondary(e.target.files[0] || null)
                }
              />
              <button
                className="btn btn-outline-primary"
                onClick={() => handleUpload(activeTab)}
                disabled={uploading}
              >
                {uploading ? "Uploading..." : "Upload Excel"}
              </button>
            </div>
          </div>
        </div>

        <div className="card-body table-responsive">
          <table className="table table-striped">
            <thead>
              <tr>
                <th>School</th>
                <th>District</th>
                <th>Registration status</th>
                <th>Year</th>
                <th>Enrollment breakdown</th>
                <th>Teacher data breakdown</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(school => (
                <tr key={school.id}>
                  <td>{school.name}</td>
                  <td>{school.district}</td>
                  <td>{school.registration_status}</td>
                  <td>{school.year}</td>
                  <td>
                    {activeTab === "secondary"
                      ? renderGradesCell(secGradesBySchool.get(school.id) || [])
                      : renderGradesCell(priGradesBySchool.get(school.id) || [])}
                  </td>
                  <td>
                    {activeTab === "secondary"
                      ? renderTeachersCell(secTeachersBySchool.get(school.id) || [])
                      : renderTeachersCell(priTeachersBySchool.get(school.id) || [])}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
};

export default HRpage;
