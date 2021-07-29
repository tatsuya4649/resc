import React from "react";
import { connect } from "react-redux";

import Header from "./Header";
import Main from "./Main";
import Footer from "./Footer";

@connect((store) => {
	return {
		uploadFile: store.uploadFileReducer.logfiles,
		analyzing: store.uploadFileReducer.analyzing,
		analyzed: store.uploadFileReducer.analyzed
	};
})
class Layout extends React.Component{
	constructor(){
		super();
		this.title = "Resc Log Analyzer";
	}
        render(){
                return (
		<div>
		<Header title={this.title} />
		<Main />
		<Footer />
		</div>
                );
        }
}

export default Layout;
