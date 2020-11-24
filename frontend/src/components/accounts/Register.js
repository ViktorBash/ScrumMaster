import React, {Component} from "react";
import {Link, Redirect} from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import {login, register} from "../../actions/auth";
import {Login} from "./Login";
import {createMessage} from "../../actions/messages";

export class Register extends Component {
    state = {
        username: "",
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        password2: ""
    };

    static propTypes = {
        register: PropTypes.func.isRequired,
        isAuthenticated: PropTypes.bool
    }

    onSubmit = e => {
        e.preventDefault();
        const { username, first_name, last_name, email, password, password2 } = this.state;

        // Make sure passwords match
        if (password !== password2) {
            this.props.createMessage({ passwordNotMatch: "Passwords do not match"})
        }
        else { // Passwords do match
            const newUser = {
                username,
                first_name,
                last_name,
                password,
                email,
            }
            this.props.register(newUser);
        }
    }

    onChange = e => this.setState({[e.target.name]: e.target.value});  // Keep state updated with input in form

    render() {
        if(this.props.isAuthenticated) {
            return <Redirect to="/" />;
        }
        const { username, email, first_name, last_name, password, password2 } = this.state;
        return (
            // Register form
            <div className="col-md-6 m-auto">
                <div className="card card-body mt-5">
                    <h2 className="text-center">Register</h2>
                    <form onSubmit={this.onSubmit}>
                        <div className="form-group">
                            <label>Username</label>
                            <input
                                type="text"
                                className="form-control"
                                name="username"
                                onChange={this.onChange}
                                value={username}
                            />
                        </div>
                        <div className="form-group">
                            <label>First Name</label>
                            <input
                                type="text"
                                className="form-control"
                                name="first_name"
                                onChange={this.onChange}
                                value={first_name}
                            />
                        </div>
                        <div className="form-group">
                            <label>Last Name</label>
                            <input
                                type="text"
                                className="form-control"
                                name="last_name"
                                onChange={this.onChange}
                                value={last_name}
                            />
                        </div>
                        <div className="form-group">
                            <label>Email</label>
                            <input
                                type="email"
                                className="form-control"
                                name="email"
                                onChange={this.onChange}
                                value={email}
                            />
                        </div>
                        <div className="form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                className="form-control"
                                name="password"
                                onChange={this.onChange}
                                value={password}
                            />
                        </div>
                        <div className="form-group">
                            <label>Confirm Password</label>
                            <input
                                type="password"
                                className="form-control"
                                name="password2"
                                onChange={this.onChange}
                                value={password2}
                            />
                        </div>
                        <div className="form-group">
                            <button type="submit" className="btn btn-primary">
                                Register
                            </button>
                        </div>
                        <p>
                            Already have an account? <Link to="/login">Login</Link>
                        </p>
                    </form>
                </div>
            </div>
        )
    }
}

const mapStateToProps = state => ({
     isAuthenticated: state.auth.isAuthenticated
    });

export default connect(mapStateToProps, { register, createMessage })(Register);