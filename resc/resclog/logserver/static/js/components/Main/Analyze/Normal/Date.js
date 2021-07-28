import React from "react";

export default class Date extends React.Component{
	element(){
		if (this.props.content.length>0){
			return (
			<div className="normal_date">
			<h4 className="normal_element">date</h4>
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
