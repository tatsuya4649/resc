import React from "react";

export default class File extends React.Component{
	element(){
		if (this.props.content.length>0){
			return (
			<div className="normal_file">
			<h4 className="normal_element">script file</h4>
			<p>{this.props.content}</p>
			<p>{this.props.binary}</p>
			</div>
			);
		}else{
			return null;
		}
	}
	render(){
		return this.element();
	}
}
