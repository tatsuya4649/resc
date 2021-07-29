import React from "react";

export default class Stdout extends React.Component{
	element(){
		if (this.props.content.length>0){
			return (
			<div className="normal_stdout">
			<h4 className="normal_element">stdout</h4>
			<p>{this.props.content}</p>
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
