import React from "react";
import { connect } from "react-redux";

import Header from "./Header";
import Main from "./Main";
import Footer from "./Footer";

@connect((store) => {
	return {
		uploadFile: store.uploadFile.logfiles,
		analyzing: store.uploadFile.analyzing,
		analyzed: store.uploadFile.analyzed
	};
})
class Layout extends React.Component{
        render(){
                return (
		<div>
		<Header title={"Hello"} />
		<Main />
		<Footer />
		</div>
                );
        }
}

export default Layout;
