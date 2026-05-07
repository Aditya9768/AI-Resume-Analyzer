import { useState } from "react";
import axios from "axios";
import Sidebar from "./components/Sidebar";
import { BarChart, Bar, XAxis, YAxis, Tooltip, LabelList, ResponsiveContainer } from "recharts";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [matchResult, setMatchResult] = useState(null);
  const [activeTab, setActiveTab] = useState("upload")

  const uploadResume = async () => {
    if (!file) return alert("Please select a file first.");

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      "http://127.0.0.1:8000/upload-resume/",
      formData
    );

    setResult(res.data);
  };

  const matchJob = async () => {
    if (!result) return alert("Please analyze a resume first.");

    const res = await axios.post(
      "http://127.0.0.1:8000/match-job/",
      {
        resume_id: result.id,
        job_description: jobDesc
      }
    );

    setMatchResult(res.data);
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    // Clear previous results
    setResult(null);
    setMatchResult(null);
  };

  return (
    <div className="flex">
      <Sidebar />

      <div className="flex-1 bg-gray-100 min-h-screen p-8">
        <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

        {/* Upload Card */}
        <div className="bg-white p-6 rounded-xl shadow mb-6">
          <h2 className="font-semibold mb-3">Upload Resume</h2>
          <input type="file" onChange={handleFileChange} />
          <button
            onClick={uploadResume}
            className="ml-3 bg-indigo-600 text-white px-4 py-2 rounded"
          >
            Analyze
          </button>
        </div>

        {/* ATS Score */}
        {result && (
          <div className="bg-white p-6 rounded-xl shadow mb-6">
            <h2 className="text-xl font-bold">ATS Score: {result.ats_score}</h2>
          </div>
        )}

        {/* Skills Chart */}
        {result && (
          <div className="bg-white p-6 rounded-xl shadow mb-6">
            <h3 className="font-semibold mb-3">Detected Skills</h3>
            <div className="flex flex-wrap gap-2">
              {Object.keys(result.skills).map((skill, index) => (
                <span
                  key={index}
                  className="bg-indigo-500 text-white px-3 py-1 rounded-full text-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Job Match */}
        {result && (
          <div className="bg-white p-6 rounded-xl shadow">
            <h3 className="font-semibold mb-2">Job Description</h3>
            <textarea
              rows="5"
              className="w-full border p-2 rounded"
              onChange={(e) => setJobDesc(e.target.value)}
            />

            <button
              onClick={matchJob}
              className="mt-3 bg-green-600 text-white px-4 py-2 rounded"
            >
              Match Resume
            </button>

            {matchResult && (
              <div className="bg-white p-6 rounded-xl shadow mt-6">
                <h2 className="text-xl font-bold text-purple-600">
                  Match Score: {matchResult.match_score}%
                </h2>

                <h3 className="mt-4 font-semibold">Resume vs Job Skills</h3>

                {matchResult?.skill_chart && (
                  <ResponsiveContainer
                    width="100%"
                    height={matchResult.skill_chart.length * 40} // 🔥 KEY FIX
                  >
                    <BarChart
                      data={matchResult.skill_chart}
                      layout="vertical"
                      margin={{ top: 10, right: 30, left: 150, bottom: 10 }}
                    >
                      <XAxis type="number" />
                      <YAxis dataKey="skill" type="category" width={150} />
                      <Tooltip />
                      <Bar dataKey="score" fill="#6366f1" minPointSize={5}>
                        <LabelList
                          dataKey="skill"
                          position="insideLeft"
                          style={{ fill: "white", fontSize: 12 }}
                        />
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                )}

                <h3 className="mt-4 font-semibold">Missing Skills</h3>
                <ul className="list-disc ml-6">
                  {matchResult.missing_skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;