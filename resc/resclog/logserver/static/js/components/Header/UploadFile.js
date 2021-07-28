import React from "react";
import { connect } from "react-redux";
import { analyzeFile } from "../../actions/UploadFile";

@connect((store)=>{
	return {
	analyzing: store.uploadFile.analyzing,
	analyzed: store.uploadFile.analyzed,
	error: store.uploadFile.error,
	};
})
export default class UploadFile extends React.Component{
	analyze(e){
		const file = e.target.files[0];
		console.log(file);
		this.props.dispatch(analyzeFile(file));
	}
	analyzing_text(){
		var result = null;
		if (this.props.analyzing == true){
			result = (
			<p>Now analyzing log...</p>
			);
		}else if (this.props.analyzed == true){
			result = (
			<p>Result of analyzed RescLog.</p>
			);
		}else if (this.props.error == true){
			result = (
			<p>Occured error.Please retry.</p>
			);
		}else{
			result = (
			<p>Select RescLog file.</p>
			);
		}
		return result;
	}
	render(){
		return (
		<div className="upload_box">
		{this.analyzing_text()}
		<div className="upload_title">
			<input name="resclog" type="file" accept="text" onChange={this.analyze.bind(this)} />
		</div>
		</div>
		);
	}
}
