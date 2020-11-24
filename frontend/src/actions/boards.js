import axios from "axios";
import {createMessage, returnErrors} from "./messages";

import {
    GET_BOARDS, CREATE_BOARD, UPDATE_BOARD, DELETE_BOARD,
    GET_BOARD_INFO,
    CREATE_SHARED_USER, DELETE_SHARED_USER,
    CREATE_TASK, UPDATE_TASK, DELETE_TASK,
} from "./types";
import {tokenConfig} from "./auth";

// Get all the applicable boards
export const getBoards = () => (dispatch, getState) => {
    axios.get("/api/board/list/", tokenConfig(getState))
        .then(res => {
            dispatch({
                type: GET_BOARDS,
                payload: res.data
            })
        })
        .catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

// Create a board
export const createBoard = (board) => (dispatch, getState) => {
    axios.post("/api/board/create/", board, tokenConfig(getState))
        .then(res => {
            dispatch(createMessage({createBoard: "Board Created"}))
            dispatch({
                type: CREATE_BOARD,
                payload: res.data
            })
        })
        .catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}
