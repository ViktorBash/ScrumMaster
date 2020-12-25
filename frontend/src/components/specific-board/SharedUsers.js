import React, { Component, Fragment } from "react";

export class SharedUsers extends Component {
    render() {
        // shared_users: Prop that is all of the shared users in a list
        return(
            <Fragment>
                <ul className="list-group">
                    {this.props.shared_users.map(shared_user => (
                        <li key={shared_user.id} className="list-group-item">
                            {shared_user.username + ": " + shared_user.email} <button className="btn btn-danger btn-sm float-right">Delete</button></li>
                    ))}
                </ul>

            </Fragment>
        )
    }
}