import React from "react";
import { Link } from "react-router-dom";
import * as SFlag from "../../../analyze/sflag";
import Date from "./Date";
import Content from "./Content";

export default class Eme extends React.Component{
	getcontent(){
		const content = this.props.analyze.err_content;
		if (content == null || content.length == 0){
			return null;
		}else{
			return <Content content={content} />;
		}
	}

	render(){
		const explains = SFlag.getflag_exlist(this.props.analyze.sflag);
		return (
		<div className="emrgency_box">
		<Link to={{pathname:"/detail",state:{analyze: this.props.analyze,index: this.props.index}}}><h3 className="eme_h3">{SFlag.getresult(this.props.analyze.sflag)}</h3></Link>
			
			<Date date={this.props.analyze.date_content} />
			<div className="ul_box">
			<ul className="ana_ul">
			{
			explains.map((explain,index)=>{
			return (<li className="anal_li" key={index}>{explain}</li>);
			})
			}
			</ul>
			</div>
			{this.getcontent()}
		</div>
		);
	}
}
