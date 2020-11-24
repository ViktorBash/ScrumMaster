// Root reducer is meeting place for all of the reducers
import {combineReducers} from "redux";
import boards from "./boards";
import errors from "./errors";
import messages from "./messages";
import auth from "./auth";

export default combineReducers({
    boards,
    errors,
    messages,
    auth
});