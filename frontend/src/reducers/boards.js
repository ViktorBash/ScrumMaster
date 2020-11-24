import {
    GET_BOARDS, CREATE_BOARD, UPDATE_BOARD, DELETE_BOARD,
    GET_BOARD_INFO,
    CREATE_SHARED_USER, DELETE_SHARED_USER,
    CREATE_TASK, UPDATE_TASK, DELETE_TASK,

} from "../actions/types";

const initialState = {
    boards: {}
}

export default function(state = initialState, action) {
    switch(action.type) {
        case "GET_BOARDS":
            return {
                ...state,
                boards: action.payload
            }
        case "CREATE_BOARD":
            // Cloning new state, then adding the board to it, finally sending it back via return{} statement
            let newState = JSON.parse(JSON.stringify(state.boards))
            newState.owned_boards.push(action.payload.board)
            return {
                ...state,
                boards: newState
            }
        default:
            return state;
    }
}