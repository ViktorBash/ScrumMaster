import React, { Component, Fragment } from "react";
import {Link} from "react-router-dom";

export class Tasks extends Component {
    // Tasks is passed "tasks" as a prop which is the list of tasks

    render() {
        return(
            <Fragment>
                    <h2>Tasks</h2>
                    <table className="table table-striped">
                        <thead>
                        <tr>
                            <th>Title</th>
                            <th>Description</th>
                            <th>Priority</th>
                            <th/>
                        </tr>
                        </thead>
                        <tbody>
                        {this.props.tasks.map(task => (
                            <tr key={task.id}>
                                <td>{task.title}</td>
                                <td>{task.description}</td>
                                <td>{task.priority}</td>
                                <td><button className="btn btn-primary btn-sm">Update</button></td>
                                <td><button className="btn btn-danger btn-sm">Delete</button></td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </Fragment>
        )
    }
}