import * as UploadFileType from "../types/UploadFile";

export default function reducer(state={
	logfiles: [],
	analyzing: false,
	analyzed: false,
	results: [],
	error: null
},action){
	switch (action.type){
	case UploadFileType.ANALYZING:
		return {...state,analyzing: true,error: false}
	case UploadFileType.ANALYZED:
		return {...state,results: [...state.results,...action.payload],logfiles: [...state.logfiles,action.logfile],analyzing: false,analyzed: true,error: false}
	case UploadFileType.ERROR:
		return {...state,analyzing: false,analyzed: false,error: true}
	}
	return state;
}

