import React, { Fragment, Component } from 'react';
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getBoard } from "../../actions/boards";
import { BoardTitleForm } from "./BoardTitleForm";
import {SharedUserForm} from "./SharedUserForm";
import {SharedUsers} from "./SharedUsers";
import {TaskForm} from "./TaskForm";
import {Tasks} from "./Tasks";

export class BoardDashboard extends Component {
    static propTypes = {
        getBoard: PropTypes.func.isRequired,
        boards: PropTypes.object.isRequired,
        isAuthenticated: PropTypes.bool,
        isLoading: PropTypes.bool,
        auth: PropTypes.object,
        isOnSpecificBoard: PropTypes.bool,
    }

    componentDidMount() {
        // .substring(7) is used to get rid of the /boards/ in front of the URL we send to getBoard()
        if(this.props.isAuthenticated && !this.props.isLoading){
            this.props.getBoard(this.props.match.url.substring(7), this.props.auth.user.id)
        }
    }

    render() {
        // If isOnASpecificBoard === true, then we the props we need to load the board
        if(this.props.isOnSpecificBoard){
            // We have to render a board we own in the owned_boards array
            if(this.props.boards.owned_boards.length === 1){
                return(
                <Fragment>
                    <h1>{this.props.boards.owned_boards[0].title}</h1>

                </Fragment>
                        )
            }
            // We have to render a shared board we are shared to in the shared_boards array
            else{
                return(
                <Fragment>
                    <h1>{this.props.boards.shared_boards[0].title}</h1>
                </Fragment>
                        )
            }

        }
        // Props have not loaded yet
        return(
            <Fragment>
                <h1>Loading</h1>
            </Fragment>
        )
    }
}
function mapStateToProps(state) {
    return { boards: state.boards.boards,
    isAuthenticated: state.auth.isAuthenticated,
        isLoading: state.auth.isLoading,
        auth: state.auth,
        isOnSpecificBoard: state.boards.boards.isOnSpecificBoard,
    }
}
export default connect(mapStateToProps, { getBoard })(BoardDashboard);