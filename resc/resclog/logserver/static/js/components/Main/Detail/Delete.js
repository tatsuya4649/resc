import React from "react";
import {connect} from "react-redux";
import { delete_index } from "../../../actions/Delete";

@connect((store)=>{
	return {
	deleting: store.uploadFileReducer.deleting,
	deleted: store.uploadFileReducer.deleted,
	delete_error: store.uploadFileReducer.delete_error,
	};
})
export default class Delete extends React.Component{
	delete_log(){
		this.props.dispatch(delete_index(this.props.index));
	}
	delete_error(){
		if (this.props.delete_error == true){
			return "Error.Retry Deleting?"
		}else{
			return "Delete this from log."
		}
	}
	render(){
		return (
		<div className="delete_box">
		<button onClick={this.delete_log.bind(this)}>{this.delete_error()}</button>
		</div>
		);
	}
}
