import React, { Component } from "react";
import "../../Styles/TraineeReport.css";
import logo from "../../images/logo.png";
import "../../Styles/Navbar.css";
import axios from "axios";
import EmployeeRow from "./EmployeeRow";

export default class TraineeReport extends Component {

	constructor(props) {
		super(props);
		this.state = { employee: [], search: "" };
		// this.state.Station = this.props.match.params.id;

		this.onChangeSearch = this.onChangeSearch.bind(this);
	}	

	onChangeSearch(e) {
		this.setState({
			search: e.target.value,
		});
	}

	componentDidMount() {
		// alert('email is ' +this.props.match.params.id);
		axios
			.get("http://127.0.0.1:8000/notes")
			.then((response) => {
				// alert('Pass una')
				// alert('Data Tika :'+response.data)
				this.setState({ employee: response.data });
			})
			.catch(function (error) {
				console.log(error);
			});
	}
	tabRow() {
		return this.state.employee.map(function (object, i) {
			return <EmployeeRow obj={object} key={i} />;
		});
		
	}

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
							<th>Joined Date</th>
							<th>Defect Rate</th>
							
							<th>Action</th>
						
						</tr>
					</thead>
					<tbody>
						{/* <tr>
							<td>sample</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
							<td>sample data</td>
						
							<td>
								<button>Delete</button>
								<button>Defect</button>
							</td>
						</tr> */}
					{this.tabRow()}
					</tbody>
				</table>
			</div>
		);
	}
}
