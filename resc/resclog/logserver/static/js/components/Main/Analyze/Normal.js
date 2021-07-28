import React from "react";
import * as SFlag from "../../../analyze/sflag";
import Date from "./Normal/Date";
import Over from "./Normal/Over";
import File from "./Normal/File";
import Func from "./Normal/Func";
import Remo from "./Normal/Remo";
import Sour from "./Normal/Sour";
import Stdout from "./Normal/Stdout";
import Stderr from "./Normal/Stderr";

export default class Normal extends React.Component{

	render(){
		console.log();
		const explains = SFlag.getflag_exlist(this.props.analyze.sflag);
		return (
		<div className="normal_box">
		<h2 className="normal_h3">normal</h2>
		<div className="ul_box">
		<ul className="ana_ul">
		{
		explains.map((explain,index)=>{
			return (
		<li className="anal_li" key={index}>{explain}</li>
		);
		})
		}
		</ul>
		<Date content={this.props.analyze.date_content} binary={this.props.analyze.date_binary} />
		<Over content={this.props.analyze.over_content} binary={this.props.analyze.over_binary} />
		<File content={this.props.analyze.file_content} binary={this.props.analyze.file_binary} />
		<Func content={this.props.analyze.func_content} binary={this.props.analyze.func_binary} />
		<Remo content={this.props.analyze.remo_content} binary={this.props.analyze.remo_binary} />
		<Sour content={this.props.analyze.sour_content} binary={this.props.analyze.sour_binary} />
		<Stdout content={this.props.analyze.stdout_content} />
		<Stderr content={this.props.analyze.stderr_content} />
		</div>
		</div>
		);
	}
}
