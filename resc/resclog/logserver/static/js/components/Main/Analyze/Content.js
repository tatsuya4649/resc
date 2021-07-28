import React from "react";

export default class Content extends React.Component{
	render(){
		return (
		<div className="ana_con">
			{this.props.content}
		</div>
		);
	}
}
