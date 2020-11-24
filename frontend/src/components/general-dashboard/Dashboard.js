import React, { Fragment } from 'react';
import Boards from "./Boards";
import Form from "./Form";

export default function Dashboard() {
    return (
        <Fragment>
            <Form/>
            <Boards/>
        </Fragment>
    )
}