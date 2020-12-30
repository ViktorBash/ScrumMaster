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
        case "UPDATE_BOARD":
            let newState2 = JSON.parse(JSON.stringify(state.boards))
            // Since we are updating the board title, we are on the page of that board
            // Therefore, there is only one board in the owned_boards array at this point
            // So instead of having to loop and change the title based on ID or url, we can just change
            // the only board that is in owned boards
            newState2.owned_boards[0].title = action.payload.title
            return {
                ...state,
                boards: newState2,
            }
        case "GET_BOARD_INFO":
            let newState3 = JSON.parse(JSON.stringify(state.boards))
            // Need to check if we are the owner of the board we received in the payload. If it is, then we add it to
            // owned boards, else we add it to shared boards.
            newState3.boards = {}
            if(action.payload.response.owner.id === action.payload.user_id) {
                newState3.boards.owned_boards = [action.payload.response]
                newState3.boards.shared_boards = []
            }
            else{
                newState3.boards.shared_boards = [action.payload.response]
                newState3.boards.owned_boards = []
            }
            newState3.boards.isOnSpecificBoard = true
            return {
                ...state,
                boards: newState3.boards,
            }
        default:
            return state;
    }
}
