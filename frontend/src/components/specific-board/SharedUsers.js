import React, { Component, Fragment } from "react";

export class SharedUsers extends Component {
    render() {
        // shared_users: Prop that is all of the shared users in a list
        console.log(this.props.shared_users)
        return(
            <Fragment>
                <ul className="list-group">
                    {this.props.shared_users.map(shared_user => (
                        <li className="list-group-item">{shared_user.username + ": " + shared_user.email}</li>
                    ))}
                </ul>

            </Fragment>
        )
    }
}