import axios from "axios";
import { returnErrors} from "./messages";

import {
    USER_LOADING,
    USER_LOADED,
    AUTH_ERROR, LOGIN_SUCCESS, LOGIN_FAIL, LOGOUT_SUCCESS, REGISTER_FAIL, REGISTER_SUCCESS
} from "./types";

// Check token & load user
export const loadUser = () => (dispatch, getState) => {

    axios.get("/api/auth/user", tokenConfig(getState))
        .then(res => {
            dispatch({
                type: USER_LOADED,
                payload: res.data
            })
        })
        .catch(err => {
            dispatch(returnErrors(err.response.data, err.response.status));
            dispatch({
                type: AUTH_ERROR
            });
        })
}

// Login user
export const login = (username, password) => (dispatch) => {

    // Headers
    const config = {
        headers: {
            "Content-Type": "application/json"
        }
    }

    // Request Body
    const body = JSON.stringify({username, password});


    axios.post("/api/auth/login/", body, config)
        .then(res => {
            dispatch({
                type: LOGIN_SUCCESS,
                payload: res.data
            })
        })
        .catch(err => {
            dispatch(returnErrors(err.response.data, err.response.status));
            dispatch({
                type: LOGIN_FAIL
            });
        })
}

// REGISTER User
export const register = ({ username, first_name, last_name, password, email }) => (dispatch) => {

    // Headers
    const config = {
        headers: {
            "Content-Type": "application/json"
        }
    }

    // Request Body
    const body = JSON.stringify({username, first_name, last_name, email, password});


    axios.post("/api/auth/register/", body, config)
        .then(res => {
            dispatch({
                type: REGISTER_SUCCESS,
                payload: res.data
            })
        })
        .catch(err => {
            dispatch(returnErrors(err.response.data, err.response.status));
            dispatch({
                type: REGISTER_FAIL
            });
        })
}


// Logout user
export const logout = () => (dispatch, getState) => {
    axios.post("/api/auth/logout/", null, tokenConfig(getState))
        .then(res => {
            dispatch({
                type: LOGOUT_SUCCESS,
            })
        })
        .catch(err => {
            console.log("test")
            console.log(err)
            dispatch(returnErrors(err.response.data, err.response.status));
        })
}

// Helper function to setup token
export const tokenConfig = (getState) => {
    // Get token from state
    const token = getState().auth.token;

    // Headers
    const config = {
        headers: {
            "Content-Type": "application/json"
        }
    }

    if (token) {
        config.headers['Authorization'] = `Token ${token}`;

    }

    return config;
}