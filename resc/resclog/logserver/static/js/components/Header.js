import React from "react";
import Title from "./Header/Title";
import UploadFile from "./Header/UploadFile";

export default class Header extends React.Component{
	render(){
		return (
		<header>
			<Title title={this.props.title} />
			<UploadFile />
		</header>
		);
	}
}
