import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import {updateBoard} from "../../actions/boards"


export class BoardTitleForm extends Component {
    state = {
        title: "",
    }

    static propTypes ={
        updateBoard: PropTypes.func.isRequired,
        board: PropTypes.object.isRequired,
    }

    onChange = e => this.setState({[e.target.name]: e.target.value });

    onSubmit = e => {
        e.preventDefault()
        const {title} = this.state;

        this.props.updateBoard(this.props.board.id, this.props.board.url, title)
        this.setState(
            {title: "",}
        )

    }

    render() {
        const { title } = this.state;
        return(
            <Fragment>
                <h1>Change Board Name</h1>
                <form onSubmit={this.onSubmit}>
                    <input
                    className=""
                    type="text"
                    name="title"
                    onChange={this.onChange}
                    value={title}
                    />
                    <button type="submit" className="btn btn-sm btn-success">Update</button>
                </form>
            </Fragment>
        )
    }

}
