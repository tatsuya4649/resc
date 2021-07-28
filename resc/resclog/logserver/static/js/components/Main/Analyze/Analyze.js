import React from "react";
import * as SFlag from "../../../analyze/sflag";
import Eme from "./Eme";
import Normal from "./Normal";

export default class Analyze extends React.Component{
	emeornot(){
		if ((SFlag.EME.flag & this.props.analyze.sflag) != 0){
			return <Eme analyze={this.props.analyze} />;
		}else{
			console.log(this.props.analyze);
			return <Normal analyze={this.props.analyze} />;
		}
	}
	render(){
		return this.emeornot();
	}
}
