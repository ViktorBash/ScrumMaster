import React, {Component, Fragment} from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { createBoard} from "../../actions/boards";

export class Form extends Component {
    state = {
        title: "",
    }

    static propTypes = {
        createBoard: PropTypes.func.isRequired,
    }

    onChange = e => this.setState({[e.target.name]: e.target.value });

    onSubmit = e => {
        e.preventDefault();
        const {title} = this.state;
        const board = { title };
        this.props.createBoard(board)
        this.setState(
            {title: "",}
        );
    };

    render() {
        const { title } = this.state;
        return (
            <Fragment>
                <h2>Create Board</h2>
                <form  onSubmit={this.onSubmit}>
                    <table className="table table-striped">
                        <tbody>
                            <tr>
                                <td><input className=""
                                           type="text"
                                           name="title"
                                           onChange={this.onChange}
                                           value={title}/></td>
                                <td><button type="submit" className="btn btn-sm btn-success">Create</button></td>
                            </tr>
                        </tbody>
                    </table>
                    </form>
            </Fragment>

        )
    }
}

export default connect(null, {createBoard})(Form);