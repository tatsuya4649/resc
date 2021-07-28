import React from "react";

export default class Over extends React.Component{
	element(){
		if (this.props.content.length>0){
			return (
			<div className="normal_over">
			<h4 className="normal_element">over</h4>
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
