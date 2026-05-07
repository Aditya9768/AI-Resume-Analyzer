import { Link } from "react-router-dom";
import { FaFileUpload, FaChartBar, FaUserTie } from "react-icons/fa";

function Sidebar() {
  return (
    <div className="w-64 bg-indigo-700 text-white min-h-screen p-6">

      <h2 className="text-2xl font-bold mb-8">
        Resume AI
      </h2>

      <ul className="space-y-4">

        <li>
          <Link to="/" className="flex items-center gap-2">
            <FaFileUpload/>
            Upload Resume
          </Link>
        </li>

        <li>
          <Link to="/analytics" className="flex items-center gap-2">
            <FaChartBar/>
            Analytics
          </Link>
        </li>

        <li>
          <Link to="/jobmatch" className="flex items-center gap-2">
            <FaUserTie/>
            Job Match
          </Link>
        </li>

      </ul>

    </div>
  );
}

export default Sidebar;