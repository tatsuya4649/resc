import React from "react";
import {Link} from "react-router-dom";
import * as SFlag from "../analyze/sflag";
import Normal from "../components/Main/Analyze/Normal";
import Eme from "../components/Main/Analyze/Eme";

export default class AnalyzeDetail extends React.Component{
	emeornot(){
		if ((SFlag.EME.flag & this.props.location.state.analyze.sflag) != 0){
			return (
			<div className="emebox">
			<Eme analyze={this.props.location.state.analyze}  />
			</div>
			);
		}else{
			return (
			<div className="normalbox">
			<Normal analyze={this.props.location.state.analyze} />
			</div>
			);
		}
	}
	render(){
		const analyze = this.props.location.state.analyze;
		return (
			<div className="detail_content">
			<div className="title_and_back">
			<h2>Detail</h2>
			<Link to={{pathname:"/"}}>back</Link>
			</div>
			{this.emeornot()}
			</div>
		);
	}
}
