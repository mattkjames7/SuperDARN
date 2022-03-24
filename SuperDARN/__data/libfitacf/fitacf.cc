#include "libfitacf.h"



fitacf::fitacf(const char *fname, bool Verbose) {
	
	
	/* open the fitacf file */
	if (Verbose) {
		printf("Reading File: %s\n",fname);
	}
	F_ = fopen(fname,"r");
	fileExists_ = (F_ != NULL);
	if (!fileExists_) {
		printf("Failed to open %s\n",fname);
		return;
	}
	
	/* get the size of the file */
	_FileSize();
	if (Verbose) {
		printf("File Size: %ld bytes\n",FLen_);
	}

	/* count the number of records in the file */
	_CountRecords();
	if (Verbose) {
		printf("Records: %d...",nRec_);
	}

	/* Read the scalars in */
	_ReadAllScalars();
	
	/* get the total number of data values in the arrays */
	_GetTotalArrayLen();
	
	/* read the arrays */
	_ReadAllArrays();
	
	/* close the file */
	fclose(F_);
	
}

fitacf::~fitacf() {
	
	/* delete stuff that has been allocated */
	if (allocScalars_) {
		delete[] scalars_;
	}
	
	if (allocArrays_) {
		delete[] arrays_;
	}
}


void fitacf::_FileSize() {
	/* Calculate the size of the file, returning the total number of
	 * bytes contained in the file */
	rewind(F_);
	
	/* seek the end of the file */
	fseek(F_,0L,SEEK_END);
	
	/* get the offset in bytes at the end of the file */
	FLen_ = ftell(F_);
	
	/* return to the beginning of the file */
	rewind(F_);
}

void fitacf::_CountRecords() {
	/* Loop through the entire file once to count the total number of
	 * data records in it, bytes 4 to 7 (inclusive) of each record
	 * is a 32-bit integer denoting the size of that block */
	long int FPos = 0;
	int tmp;
	n_ = 0;
	rewind(F_);
	while (FPos < FLen_) {
		fseek(F_,FPos+4,SEEK_SET);
		fread(&tmp,sizeof(int),1,F_);
		n_++;
		FPos+=tmp;
	}
	rewind(F_);
}

void fitacf::_ReadString(char *str, int *len) {
	/* Read a string (of char) of length len from the file at the 
	 * current file offset*/
	len[0] = 0;
	char tmp = 1;
	while (tmp != 0) {
		fread(&tmp,sizeof(char),1,F_);
		str[len[0]] = tmp;
		len[0] += 1;
	}
}	


void fitacf::_ReadRecordHeader(int *magic, int *size, int *ns, int *na) {
	/*******************************************************************
	 * Read in the first few parameters in the record...
	 * magic : 
	 * size : number of bytes in this record
	 * ns : 
	 * na : 
	 * ****************************************************************/
	fread(magic,sizeof(int),1,F_);
	fread(size,sizeof(int),1,F_);
	fread(ns,sizeof(int),1,F_);
	fread(na,sizeof(int),1,F_);
}

	
void fitacf::_ReadRecordScalars(int ns, int I) {
	
	/* string length */
	int l;
	
	/* temporary integers for storing date/time */
	int yr, mo, dy, hr, mt, sc, us;
	
	/* string buffers */
	char strbuff[256], tmpstr[256];
	
	/* character denoting the data type */
	char dtype;
	
	/* temporary data types */
	char tmpchar;
	short int tmpshrt;
	int tmpint;
	float tmpflt;
	double tmpdbl;
	
	/* loop through the first part of the record to read each scalar in */
	int i;
	for (i=0;i<ns;i++) {
		/* read the name of the scalar */
		_ReadString(strbuff,&l);
		
		/* get the dtype, then read the value in */
		fread(&dtype,sizeof(char),1,F_);
		switch (dtype) {
			case 1:
				fread(&tmpchar,sizeof(char),1,F_);
				break;
			case 2:
				fread(&tmpshrt,sizeof(short int),1,F_);
				break;			
			case 3:
				fread(&tmpint,sizeof(int),1,F_);
				break;		
			case 4:
				fread(&tmpflt,sizeof(float),1,F_);
				break;		
			case 8:
				fread(&tmpdbl,sizeof(double),1,F_);
				break;
			default:
				_ReadString(tmpstr,&l);
		}
		
		/* set the appropriate scalars_ variable (I wonder if there's
		 * a more efficient way of doing this?) also I need to add
		 * all of the other parameters in really */
		if (strcmp(strbuff,"cp") == 0) {
			scalars_[I].ScanCode = tmpshrt;
		} else if (strcmp(strbuff,"time.yr") == 0)  {
			yr = tmpshrt;
		} else if (strcmp(strbuff,"time.mo") == 0)  {
			mo = tmpshrt;
		} else if (strcmp(strbuff,"time.dy") == 0)  {
			dy = tmpshrt;
		} else if (strcmp(strbuff,"time.hr") == 0)  {
			hr = tmpshrt;
		} else if (strcmp(strbuff,"time.mt") == 0)  {
			mt = tmpshrt;
		} else if (strcmp(strbuff,"time.sc") == 0)  {
			sc = tmpshrt;
		} else if (strcmp(strbuff,"time.us") == 0)  {
			us = tmpshrt;
		} else if (strcmp(strbuff,"lagfr") == 0)  {
			scalars_[I].lagfr = tmpshrt;
		} else if (strcmp(strbuff,"smsep") == 0)  {
			scalars_[I].smsep = tmpshrt;
		} else if (strcmp(strbuff,"channel") == 0)  {
			scalars_[I].Channel = tmpshrt;
		} else if (strcmp(strbuff,"bmnum") == 0)  {
			scalars_[I].Beam = tmpshrt;
		} else if (strcmp(strbuff,"nrang") == 0) {
			scalars_[I].nGates = tmpshrt;
		}
	}
	/* set date and time */
	scalars_[I].Date = yr*10000 + mo*100 + dy;
	scalars_[I].ut = (float) hr + ((float) mt)/60.0 + ((float) sc)/3600.0 + ((float) us)/(3600.0*1000000.0);
}


/* record index, combined output array index */
void fitacf::_ReadRecordArrays(int I, int pos) {
	
	/* seek to the offset at the start of these arrays */
	fseek(F_,scalars_[I].ArrOffset,SEEK_SET);

	/* string length */
	int l;
		
	/* string buffers */
	char strbuff[256], tmpstr[256];
	
	/* character denoting the data type */
	char dtype;
	
	/* number of array dimensions */
	int dim;
	
	/* number of elements in each dimension (unlikely to have as many
	 * as 10 dimensions */
	int rng[10];
	
	/* total number of elements in all dimensions */
	int r;

	/* temporary arrays - I guess I used 120 because that's more than
	 * the most ranges that the radars would have. It could break in 
	 * future though*/
	char tmpchar[120];
	short int tmpshrt[120];
	int tmpint[120];
	float tmpflt[120];
	double tmpdbl[120];
	
	/* the number of arrays we have read in so far */
	int nread = 0;
	
	/* loop thorugh each of the arrays int he record until we have all 5
	 * of the ones we're interested in (in future I should probably 
	 * include more */
	int i, j;
	for (i=0;i<scalars_[I].na;i++) {
		/* get the name of the array */
		_ReadString(strbuff,&l);
		
		/* read the datatype character */
		fread(&dtype,sizeof(char),1,F_);
		
		/* the number of dimensions */
		fread(&dim,sizeof(int),1,F_);
		
		/* the number of elements in each dimension */
		fread(&rng,sizeof(int),dim,F_);
		
		/* calculate the total number of elements from each dimension */
		r = rng[0];
		for (j=1;j<dim;j++) {
			r *= rng[j];
		}
		
		/* read the data into a temporary variable */
		switch ((int) dtype) {
			case 1:
				fread(tmpchar,sizeof(char),r,F_);
				break;
			case 2:
				fread(tmpshrt,sizeof(short int),r,F_);
				break;			
			case 3:
				fread(tmpint,sizeof(int),r,F_);
				break;		
			case 4:
				fread(tmpflt,sizeof(float),r,F_);
				break;		
			case 8:
				fread(tmpdbl,sizeof(double),r,F_);
				break;
			default:
				for (j=0;j<r;j++) {
					_ReadString(tmpstr,&l);
				}
				
		}
		
		/* this bit will copy the temp variables into the arrays_
		 * struct stored within the object. (perhaps this could be done 
		 * within the case statment above to slightly improve speed) */
		if (strcmp(strbuff,"v") == 0) {
			for (j=0;j<scalars_[I].ArrLen;j++){
				V[sp+j] = tmpflt[j];
				nread++;
			}
		} else if (strcmp(strbuff,"p_l") == 0)  {
			for (j=0;j<scalars_[I].ArrLen;j++){
				P_l[sp+j] = tmpflt[j];
				nread++;
			}
		} else if (strcmp(strbuff,"w_l") == 0)  {
			for (j=0;j<scalars_[I].ArrLen;j++){
				W_l[sp+j] = tmpflt[j];
				nread++;
			}
		} else if (strcmp(strbuff,"gflg") == 0)  {
			for (j=0;j<scalars_[I].ArrLen;j++){
				Gnd[sp+j] = tmpchar[j];
				nread++;
			}
		} else if (strcmp(strbuff,"slist") == 0)  {
			for (j=0;j<scalars_[I].ArrLen;j++){
				Gate[sp+j] = tmpshrt[j];
				nread++;
			}
		} 
		if (nread == 5){
			/* we have everything, leave the loop */
			break;
		}
	}
	
}	

void fitacf::_GetTotalArrayLen() {
	int i;
	n_ = 0;
	for (i=0;i<*nRec_;i++) {
		if (scalars_[i].ArrLen == 0) {
			n_++;
		} else {
			n_ += scalars_[i].ArrLen;
		}
	}
}

int fitacf::_GetArrayLen(long int FileOffset, int na) {
	
	/* seek to the beginning of the arrays */
	fseek(F,FileOffset,SEEK_SET);

	/* string length */
	int l;
		
	/* string buffers */
	char strbuff[256], tmpstr[256]
	
	/* character denoting the data type */
	char dtype;
	
	/* number of array dimensions */
	int dim;
	
	/* number of elements in each dimension (unlikely to have as many
	 * as 10 dimensions */
	int rng[10];
	
	/* total number of elements in all dimensions */
	int r;

	/* temporary arrays - I guess I used 120 because that's more than
	 * the most ranges that the radars would have. It could break in 
	 * future though*/
	char tmpchar[120];
	short int tmpshrt[120];
	int tmpint[120];
	float tmpflt[120];
	double tmpdbl[120];
	
	/* loop through the arrays until we find one of the 5 which we want
	 * (they all have the same length) */
	int i, j;
	for (i=0;i<na;i++) {
		/* get the name of the array */
		_ReadString(F_,strbuff,&l);
		
		/* read the datatype character */
		fread(&dtype,sizeof(char),1,F_);
		
		/* the number of dimensions */
		fread(&dim,sizeof(int),1,F_);
		
		/* the number of elements in each dimension */
		fread(&rng,sizeof(int),dim,F_);
		
		/* calculate the total number of elements from each dimension */
		r = rng[0];
		for (j=1;j<dim;j++) {
			r *= rng[j];
		}

		/* check if we have found one which we want (and return the size) */
		if (strcmp(strbuff,"v") == 0) {
			return r;
		} else if (strcmp(strbuff,"p_l")  == 0) {
			return r;
		} else if (strcmp(strbuff,"w_l") == 0)  {
			return r;
		} else if (strcmp(strbuff,"gflg") == 0)  {
			return r;
		} else if (strcmp(strbuff,"slist") == 0)  {
			return r;
		} 		
		
		/* read the data into a temporary variable */
		switch ((int) dtype) {
			case 1:
				fread(tmpchar,sizeof(char),r,F_);
				break;
			case 2:
				fread(tmpshrt,sizeof(short int),r,F_);
				break;			
			case 3:
				fread(tmpint,sizeof(int),r,F_);
				break;		
			case 4:
				fread(tmpflt,sizeof(float),r,F_);
				break;		
			case 8:
				fread(tmpdbl,sizeof(double),r,F_);
				break;
			default:
				for (j=0;j<r;j++) {
					ReadString(F_,tmpstr,&l);
				}
				
		}
	}
	return 0;
}	


void fitacf::_ReadAllScalars() {

	/* allocate scalars */
	scalars_ = new scalars[nRec_];
	allocScalars_ = true;

	int i;
	long int p;
	int magic, size, ns;
	p = 0;
	/* loop through each record */
	for (i=0;i<nRec_;i++) {
		/* seek the correct position in the file at the start of the 
		 * record */
		fseek(F,p,SEEK_SET);
		
		/* read in the header */
		_ReadRecordHeader(F,&magic,&size,&ns,&scalars_[i].na);
		
		/* read some more scalars in */
		_ReadRecordScalars(ns,i);
		
		/* We should be at the start of the arrays now, note the offset*/
		scalars_[i].ArrOffset = ftell(F);
		
		/* get the number of array elements */
		scalars_[i].ArrLen = _GetArrayLen(scalars_[i].ArrOffset,scalars_[i].na);
		
		/* and finally the size of this record in bytes */
		scalars_[i].RecLen = size;
		p += size;
	}
}


void fitacf::_ReadAllArrays() {
	
	/* allocate arrays */
	arrays_ = new arrays[n_];
	allocArrays_ = true;

	/* loop through all of the records */
	int i, j;
	long int p = 0;		
	for (i=0;i<nRec_;i++) {
		if (scalars_[i].ArrLen > 0) {
			/* fill in some stuff that comes from the scalars */
			for (j=0;j<scalars_[i].ArrLen;j++) {
				arrays_[p+j].Date = scalars_[i].Date;
				arrays_[p+j].ut = scalars_[i].ut;
				arrays_[p+j].Beam = scalars_[i].Beam;
				arrays_[p+j].Channel = scalars_[i].Channel;
				arrays_[p+j].ScanCode = scalars_[i].ScanCode;
				arrays_[p+j].nGates = scalars_[i].nGates;
				arrays_[p+j].lagfr = scalars_[i].lagfr;
				arrays_[p+j].smsep = scalars_[i].smsep;
			}
			/* read the arrays in from the record */
			_ReadRecordArrays(i,p);
			p += scalars_[i].ArrLen;
		} else {
			/* fill with a NAN */
			arrays_[p].Date = scalars_[i].Date;
			arrays_[p].ut = scalars_[i].ut;
			arrays_[p].Beam = scalars_[i].Beam;
			arrays_[p].Channel = scalars_[i].Channel;
			arrays_[p].ScanCode = scalars_[i].ScanCode;
			arrays_[p].nGates = scalars_[i].nGates;
			arrays_[p].lagfr = scalars_[i].lagfr;
			arrays_[p].smsep = scalars_[i].smsep;
			arrays_[p].V[p] = 	NAN;
			arrays_[p].P_l[p] = NAN;
			arrays_[p].W_l[p] = NAN;
			arrays_[p].Gnd[p] = 0;
			arrays_[p].Gate[p] = -1;		
			p++;
		}
	}		
}

int fitacf::GetScalarLen() {
	return nRec_;
}

void fitacf::GetScalars(int *Date, float *ut, int *Beam, int *Channel,
						int *ScanCode, int *nGates, int *smsep, 
						int *lagfr, int *ArrLen, int *RecLen, int *na, 
						long int *ArrOffset) {
	int i;
	for (i=0;i<nRec_;i++) {
		Date[i] = scalars_[i].Date;
		ut[i] = scalars_[i].ut;
		Beam[i] = scalars_[i].Beam;
		Channel[i] = scalars_[i].Channel;
		ScanCode[i] = scalars_[i].ScanCode;
		nGates[i] = scalars_[i].nGates;
		smsep[i] = scalars_[i].smsep;
		lagfr[i] = scalars_[i].lagfr;
		ArrLen[i] = scalars_[i].ArrLen;
		RecLen[i] = scalars_[i].RecLen;
		na[i] = scalars_[i].na;
		ArrOffset[i] = scalars_[i].ArrOffset;
	}
}

int fitacf::GetArrayLen() {
	return n_;
}

void fitacf::GetArrays(	int *Date, float *ut, int *Beam, int *Channel,
						int *ScanCode, int *nGates, int *smsep, 
						int *lagfr, float *V, float *P_l, float *W_l,
						int *Gnd, int *Gate) {
	int i;
	for (i=0;i<n_;i++) {
		Date[i] = arrays_[i].Date;
		ut[i] = arrays_[i].ut;
		Beam[i] = arrays_[i].Beam;
		Channel[i] = arrays_[i].Channel;
		ScanCode[i] = arrays_[i].ScanCode;
		nGates[i] = arrays_[i].nGates;
		smsep[i] = arrays_[i].smsep;
		lagfr[i] = arrays_[i].lagfr;
		V[i] = arrays_[i].V;
		P_l[i] = arrays_[i].P_l;
		W_l[i] = arrays_[i].W_l;
		Gnd[i] = arrays_[i].Gnd;
		Gate[i] = arrays_[i].Gate;
	}
}

