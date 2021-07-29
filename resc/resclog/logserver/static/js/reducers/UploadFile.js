import * as UploadFileType from "../types/UploadFile";
import * as DeleteType from "../types/Delete";

export default function reducer(state={
	logfiles: [],
	analyzing: false,
	analyzed: false,
	deleting: false,
	deleted: false,
	results: [],
	error: null,
	delete_error: false
},action){
	switch (action.type){
	case UploadFileType.ANALYZING:
		return {...state,analyzing: true,error: false}
	case UploadFileType.ANALYZED:
		return {...state,results: [...state.results,...action.payload],logfiles: [...state.logfiles,action.logfile],analyzing: false,analyzed: true,error: false}
	case UploadFileType.ERROR:
		return {...state,analyzing: false,analyzed: false,error: true}
	case DeleteType.DELETEALL:
		return {
		...state,
		logfiles: state.logfiles.filter((file)=>false),
		analyzing: false,
		analyzed: false,
		results: state.results.filter((res)=>false),
		delete_error: false
		}
	}
	return state;
}

