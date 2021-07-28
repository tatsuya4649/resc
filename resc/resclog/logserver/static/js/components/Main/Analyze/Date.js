import React from "react";

export default class Date extends React.Component{
	render(){
		return (
		<div className="date_box">
		<span className="date_font">{this.props.date}</span>
		</div>
		);
	}
}
