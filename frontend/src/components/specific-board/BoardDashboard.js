import React, { Fragment, Component } from 'react';
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getBoard, updateBoard } from "../../actions/boards";
import { BoardTitleForm } from "./BoardTitleForm";
import {SharedUserForm} from "./SharedUserForm";
import {SharedUsers} from "./SharedUsers";
import {TaskForm} from "./TaskForm";
import {Tasks} from "./Tasks";
import { Route, Switch, Redirect } from "react-router-dom";

export class BoardDashboard extends Component {
    static propTypes = {
        getBoard: PropTypes.func.isRequired,
        updateBoard: PropTypes.func.isRequired,
        boards: PropTypes.object.isRequired,
        isAuthenticated: PropTypes.bool,
        isLoading: PropTypes.bool,
        auth: PropTypes.object,
        isOnSpecificBoard: PropTypes.bool,
        errorMessage: PropTypes.object,
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
                    <div className="row">
                        <div className="col-lg-8">
                            <TaskForm/>
                            <Tasks tasks={this.props.boards.owned_boards[0].tasks}/>
                        </div>
                        <div className="col-lg-4">
                            <h1>Shared Users</h1>
                            <SharedUsers shared_users={this.props.boards.owned_boards[0].shared_users}/>
                            <SharedUserForm/>
                            <BoardTitleForm board={this.props.boards.owned_boards[0]} updateBoard={this.props.updateBoard}/>
                        </div>
                    </div>



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

        // Check if there is an errorMessage. If there is, then we have a 404 and should redirect to the home page.
        // Otherwise, we are just loading in and waiting for props to load.
        if(Object.keys(this.props.errorMessage).length === 0){
            return(
            <Fragment>
                <h1>Loading</h1>
            </Fragment>
        )
        }
        // 404, should redirect home or to an error screen
        return (
            <Fragment>
                <Redirect to={"/"}/>
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
        errorMessage: state.errors.msg,
    }
}
export default connect(mapStateToProps, { getBoard, updateBoard })(BoardDashboard);