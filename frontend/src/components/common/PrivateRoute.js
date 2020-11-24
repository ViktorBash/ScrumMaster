import React from "react";
import {Route, Redirect} from "react-router-dom";
import {connect} from "react-redux";
import PropTypes from "prop-types";

// Private route checks for authentication before someone can navigate to it
const PrivateRoute = ({component: Component, auth, ...rest}) => (
    <Route
        {...rest}
        render={props => {
            if(auth.isLoading) {
                return <h2>Loading...</h2>;
            }
            else if(!auth.isAuthenticated) {
                return <Redirect to="/login" />;
            }

            else {
                return <Component {...props} />;
            }
        }}

    />
);
const mapStateToProps = state => ({
    auth: state.auth
});

// Why we need this:
// https://react-redux.js.org/using-react-redux/connect-mapstate#:~:text=As%20the%20first%20argument%20passed,as%20just%20mapState%20for%20short.&text=It%20receives%20the%20entire%20store,of%20data%20this%20component%20needs.
export default connect(mapStateToProps)(PrivateRoute);
