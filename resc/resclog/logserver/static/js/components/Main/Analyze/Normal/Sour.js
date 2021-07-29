import React from "react";

export default class Sour extends React.Component{
	constructor(){
		super();
		this.tabsize = 40;
	}
	ascii(content){
		return content.match(/.*\n/g);
	}
	tab(sentence){
		// [\t\t]
	 	const result = sentence.match(/^\t+/g);
		if (result == null || result.length == 0){
			return this.tabsize*0;
		}
		// [\t,\t]
		const count = result[0].match(/\t/g);
		return this.tabsize*count.length;
	}
	element(){
		if (this.props.content.length>0){
			return (
			<div className="normal_sour">
			<h4 className="normal_element">source</h4>
			{
			this.ascii(this.props.content).map((sentence,index)=>{
				const tab = `${this.tab(sentence)}px`;
				if (this.tab(sentence)!=null ){
					return <p style={{marginLeft: tab}} className="sentence_code" key={index} >{sentence}</p>;
				}else{
					return <p className="sentence_code" key={index} >{sentence}</p>;
				}
			})
			}
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
