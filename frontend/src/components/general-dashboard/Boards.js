import React, { Component, Fragment } from 'react';
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getBoards } from "../../actions/boards";
import { Link } from "react-router-dom";


export class Boards extends Component {
    static propTypes = {
        boards: PropTypes.object.isRequired,
        getBoards: PropTypes.func.isRequired,
    };

    componentDidMount() {
        this.props.getBoards()
    }

    render() {

        // If statement to check whether the boards object is populated. If it is empty then we return nothing
        if(Object.keys(this.props.boards).length === 0) {
        return(
            <Fragment>
            </Fragment>
        )
        }
        else {
            return (

                <Fragment>
                    <h2>Boards</h2>
                    <table className="table table-striped">
                        <thead>
                        <tr>
                            <th>Name</th>
                            <th>Owner</th>
                            <th/>
                        </tr>
                        </thead>
                        <tbody>
                        {this.props.boards.owned_boards.map(board => (
                            <tr key={board.id}>
                                <td>{board.title}</td>
                                <td>{board.owner.username}</td>
                                <td>
                                    <Link to={`/board/${board.url}`}>
                                        <button className="btn btn-success btn-sm">Open</button>
                                    </Link>
                                </td>
                            </tr>
                        ))}
                        {this.props.boards.shared_boards.map(board => (
                            <tr key={board.id}>
                                <td>{board.title}</td>
                                <td>{board.owner.username}</td>
                                <td>
                                    <Link to={`/board/${board.url}`}>
                                        <button className="btn btn-success btn-sm">Open</button>
                                    </Link>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </Fragment>
            )
        }
    }
}


function mapStateToProps(state) {
    return { boards: state.boards.boards }
}


export default connect(mapStateToProps, { getBoards })(Boards);
