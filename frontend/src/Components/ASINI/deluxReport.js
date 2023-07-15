import React, { useEffect, useState } from "react";
import "../../Styles/TraineeReport.css";
import logo from "../../images/logo.png";
import "../../Styles/Navbar.css";
import axios from "axios";
import { Link, useParams, useNavigate } from "react-router-dom";

function DeluxReport() {
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
      <h2>Dexterity Report</h2>
      <Link
  className="btn btn-outline-primary mx-2"
  to={`/register`}
  style={{ position: 'absolute', top: 200, right: 30 }} // Add inline styles for positioning
>
  Employee Register
</Link>


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
              <td>{post.dRate}</td>
              <td>
                <button onClick={() => deletePost(post.id)}>Delete</button>
                <Link className="btn btn-outline-primary mx-2" to={`/ImageUploaddefect/${post.id}`}>
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

export default DeluxReport;
