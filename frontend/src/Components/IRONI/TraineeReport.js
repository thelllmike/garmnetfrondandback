import React, { Component } from "react";
import "../../Styles/TraineeReport.css";
import logo from "../../images/logo.png";
import "../../Styles/Navbar.css";

export default class TraineeReport extends Component {
	render() {
		return (
			<div className='traineeReport'>
				<header className='navbar'>
					<ul>
						<img src={logo} alt='' />
						<li>Home</li>
						<li>Progress View</li>
						<li>Progress Report</li>
						<li>Contact Us</li>
						<li>About</li>
					</ul>
				</header>
				<h2>Trainee Report</h2>
				<table className='table table-striped' style={{ marginTop: 20 }}>
					<thead>
						<tr>
							<th>Candidate ID</th>
							<th>Name</th>
							<th>Age</th>
							<th>Product No</th>
							<th>Joined Date</th>
							<th>Defect Rate</th>
							<th>Dexterity Test</th>
							<th>Button</th>
							{/* <th colSpan='3'></th> */}
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>sample</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>
								<button>btn1</button>
								<button>btn2</button>
							</td>
						</tr>
						<tr>
							<td>sample</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>
								<button>btn1</button>
								<button>btn2</button>
							</td>
						</tr>
						<tr>
							<td>sample</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>
								<button>btn1</button>
								<button>btn2</button>
							</td>
						</tr>
						<tr>
							<td>sample</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>
								<button>btn1</button>
								<button>btn2</button>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		);
	}
}
