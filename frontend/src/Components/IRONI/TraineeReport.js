import React, { useEffect, useState } from "react";
import "../../Styles/TraineeReport.css";
import logo from "../../images/logo.png";
import "../../Styles/Navbar.css";
import axios from "axios";
import { Link, useParams, useNavigate } from "react-router-dom";

function TraineeReport() {
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    const response = await axios.get("http://127.0.0.1:8000/notes");
    const postsData = response.data;
    setPosts(postsData);
  };

  const deletePost = async (id) => {
    await axios.delete(`http://127.0.0.1:8000/notes/${id}`);
    loadPosts();
	alert("Employee Successfully Deleted....")
  };

  return (
    <div className="traineeReport">
      <header className="navbar">
        <ul>
          <img src={logo} alt="" />
          <li>Home</li>
          <li>Progress View</li>
          <li>Progress Report</li>
          <li>Contact Us</li>
          <li>About</li>
        </ul>
      </header>
      <h2>Trainee Report</h2>
      <table className="table table-striped" style={{ marginTop: 20 }}>
        <thead>
          <tr>
            <th>Candidate ID</th>
            <th>Name</th>
            <th>Age</th>
            <th>Joined Date</th>
            <th>Defect Rate</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {posts.map((post, index) => (
            <tr key={index}>
              <td>{post.candidate}</td>
              <td>{post.name}</td>
              <td>{post.age}</td>
              <td>{post.joinDate}</td>
              <td>{post.rate}</td>
              <td>
                <button onClick={() => deletePost(post.id)}>Delete</button>
                <Link className="btn btn-outline-primary mx-2" to={`/imageupload/${post.id}`}>
                  Defect
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TraineeReport;
