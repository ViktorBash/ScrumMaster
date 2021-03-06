import React, {Component} from "react";
import { Link, Redirect } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { login } from "../../actions/auth";

export class Login extends Component {
    state = {
        username: "",
        password: "",
    };

    static propTypes = {
        login: PropTypes.func.isRequired,
        isAuthenticated: PropTypes.bool
    }

    onSubmit = e => {
        e.preventDefault();
        this.props.login(this.state.username, this.state.password);
        this.setState({password: ""}); // Reset password in case login not successful
    }

    onChange = e => this.setState({[e.target.name]: e.target.value}); // Keep state updated with input in the form

    render() {
        if(this.props.isAuthenticated) {
            // We check if props.location.state is undefined. If it isn't that means we got passed a URL we can use
            // to redirect the user once they are unauthenticated. Otherwise we just redirect them to home screen.
            if(this.props.location.state !== undefined) {
                return <Redirect to={this.props.location.state.url}/>
            }
            return <Redirect to="/"/>


        }
        const { username, password } = this.state;
        return (
            // Login form
            <div className="col-md-6 m-auto">
                <div className="card card-body mt-5">
                    <h2 className="text-center">Login</h2>
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
                            <button type="submit" className="btn btn-primary">
                                Login
                            </button>
                        </div>
                        <p>
                            Don't have an account? <Link to="/register">Register</Link>
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

export default connect(mapStateToProps, { login })(Login);