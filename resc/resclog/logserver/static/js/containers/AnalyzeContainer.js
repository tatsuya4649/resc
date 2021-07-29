import React from "react";
import { connect } from "react-redux";
import Analyze from "../components/Main/Analyze/Analyze";


@connect((store) => {
	return {
		anaresults: store.uploadFileReducer.results
	};
})
export default class AnalyzeContainer extends React.Component{
	length(){
		var result = null;
		if (this.props.anaresults.length > 0){
			result = <h2>Log analysis result({this.props.anaresults.length}).</h2>
		}else{
			result = null;
		}
		return result;
	}
	render(){
		return (
		<div className="analyze_container">
		{this.length()}
		{this.props.anaresults.map((analyze,index)=>{
			return <Analyze key={index} analyze={analyze} index={index} />
		})}
		</div>
		);
	}
}
