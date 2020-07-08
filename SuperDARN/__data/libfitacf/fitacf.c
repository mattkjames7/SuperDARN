#include "fitacf.h"

long int FileSize(FILE *F) {
	/* Calculate the size of the file, returning the total number of
	 * bytes contained in the file */
	long int FLen;
	rewind(F);
	fseek(F,0L,SEEK_END);
	FLen = ftell(F);
	rewind(F);
	return FLen;
}

int CountRecords(FILE *F, long int FLen) {
	/* Loop through the entire file once to count the total number of
	 * data records in it, bytes 4 to 7 (inclusive) of each record
	 * is a 32-bit integer denoting the size of that block */
	long int FPos = 0;
	int n = 0, tmp;
	rewind(F);
	while (FPos < FLen) {
		fseek(F,FPos+4,SEEK_SET);
		fread(&tmp,sizeof(int),1,F);
		n++;
		FPos+=tmp;
	}
	rewind(F);
	return n;
}


void ReadString(FILE *F,unsigned char *str, int *len) {
	/* Read a string (of char) of length len from the file at the 
	 * current file offset*/
	*len = 0;
	unsigned char tmp = 1;
	while (tmp != 0) {
		fread(&tmp,sizeof(char),1,F);
		str[*len] = tmp;
		(*len) += 1;
	}
}	

void ReadRecordHeader(FILE *F, int *magic, int *size, int *ns, int *na) {
	/*******************************************************************
	 * Read in the first few parameters in the record...
	 * magic : 
	 * size : number of bytes in this record
	 * ns : 
	 * na : 
	 * ****************************************************************/
	fread(magic,sizeof(int),1,F);
	fread(size,sizeof(int),1,F);
	fread(ns,sizeof(int),1,F);
	fread(na,sizeof(int),1,F);
}
	
void ReadRecordScalars(FILE *F, int ns, int *rDate, float *rut, int *rBeam, int *rChannel, int *rScanCode, int *rnGates, int *rlagfr, int *rsmsep) {
	int l, i, yr, mo, dy, hr, mt, sc, us;
	unsigned char strbuff[256], tmpstr[256], dtype;
	unsigned char tmpchar;
	short int tmpshrt;
	int tmpint;
	float tmpflt;
	double tmpdbl;
	for (i=0;i<ns;i++) {
		ReadString(F,strbuff,&l);
		fread(&dtype,sizeof(unsigned char),1,F);
		switch (dtype) {
			case 1:
				fread(&tmpchar,sizeof(unsigned char),1,F);
				break;
			case 2:
				fread(&tmpshrt,sizeof(short int),1,F);
				break;			
			case 3:
				fread(&tmpint,sizeof(int),1,F);
				break;		
			case 4:
				fread(&tmpflt,sizeof(float),1,F);
				break;		
			case 8:
				fread(&tmpdbl,sizeof(double),1,F);
				break;
			default:
				ReadString(F,tmpstr,&l);
		}
		
		if (strcmp(strbuff,"cp") == 0) {
			*rScanCode = tmpshrt;
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
			*rlagfr = tmpshrt;
		} else if (strcmp(strbuff,"smsep") == 0)  {
			*rsmsep = tmpshrt;
		} else if (strcmp(strbuff,"channel") == 0)  {
			*rChannel = tmpshrt;
		} else if (strcmp(strbuff,"bmnum") == 0)  {
			*rBeam = tmpshrt;
		} else if (strcmp(strbuff,"nrang") == 0) {
			*rnGates = tmpshrt;
		}
		*rDate = yr*10000 + mo*100 + dy;
		*rut = (float) hr + ((float) mt)/60.0 + ((float) sc)/3600.0 + ((float) us)/(3600.0*1000000.0);
	}
	
}

void ReadRecordArrays(FILE *F, long int FileOffset, int sp, int na, int al, float *V, float *P_l, float *W_l, int *Gnd, int *Gate) {
	fseek(F,FileOffset,SEEK_SET);
	int l, i, j, dim, rng[10], r, nread = 0;
	char strbuff[256], tmpstr[256], dtype;
	unsigned char tmpchar[120];
	short int tmpshrt[120];
	int tmpint[120];
	float tmpflt[120];
	double tmpdbl[120];
	for (i=0;i<na;i++) {
		
		ReadString(F,strbuff,&l);
		fread(&dtype,sizeof(char),1,F);
		
		fread(&dim,sizeof(int),1,F);
		fread(&rng,sizeof(int),dim,F);
		r = rng[0];
		for (j=1;j<dim;j++) {
			r *= rng[j];
		}
		switch ((int) dtype) {
			case 1:
				fread(tmpchar,sizeof(unsigned char),r,F);
				break;
			case 2:
				fread(tmpshrt,sizeof(short int),r,F);
				break;			
			case 3:
				fread(tmpint,sizeof(int),r,F);
				break;		
			case 4:
				fread(tmpflt,sizeof(float),r,F);
				break;		
			case 8:
				fread(tmpdbl,sizeof(double),r,F);
				break;
			default:
				for (j=0;j<r;j++) {
					ReadString(F,tmpstr,&l);
				}
				
		}
		
		if (strcmp(strbuff,"v") == 0) {
			for (j=0;j<al;j++){
				V[sp+j] = tmpflt[j];
				nread++;
			}
		} else if (strcmp(strbuff,"p_l") == 0)  {
			for (j=0;j<al;j++){
				P_l[sp+j] = tmpflt[j];
				nread++;
			}
		} else if (strcmp(strbuff,"w_l") == 0)  {
			for (j=0;j<al;j++){
				W_l[sp+j] = tmpflt[j];
				nread++;
			}
		} else if (strcmp(strbuff,"gflg") == 0)  {
			for (j=0;j<al;j++){
				Gnd[sp+j] = tmpchar[j];
				nread++;
			}
		} else if (strcmp(strbuff,"slist") == 0)  {
			for (j=0;j<al;j++){
				Gate[sp+j] = tmpshrt[j];
				nread++;
			}
		} 
		if (nread == 5){
			return;
		}
		//fseek(F,-2,SEEK_CUR);
	}
	
}	

int GetArrayLen(FILE *F, long int FileOffset, int na) {
	fseek(F,FileOffset,SEEK_SET);
	int l, i, j, dim, rng[10], r;
	unsigned char strbuff[256], tmpstr[256], dtype;
	unsigned char tmpchar[120];
	short int tmpshrt[120];
	int tmpint[120];
	float tmpflt[120];
	double tmpdbl[120];
	for (i=0;i<na;i++) {
		ReadString(F,strbuff,&l);
		fread(&dtype,sizeof(unsigned char),1,F);
		fread(&dim,sizeof(int),1,F);
		fread(&rng,sizeof(int),dim,F);
		r = rng[0];
		for (j=1;j<dim;j++) {
			r *= rng[j];
		}
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
		
		switch (dtype) {
			case 1:
				fread(tmpchar,sizeof(unsigned char),r,F);
				break;
			case 2:
				fread(tmpshrt,sizeof(short int),r,F);
				break;			
			case 3:
				fread(tmpint,sizeof(int),r,F);
				break;		
			case 4:
				fread(tmpflt,sizeof(float),r,F);
				break;		
			case 8:
				fread(tmpdbl,sizeof(double),r,F);
				break;
			default:
				for (j=0;j<r;j++) {
					ReadString(F,tmpstr,&l);
				}
				
		}

		
	}
	return 0;
}	


void GetScalars(FILE *F, int nRec, int *RecLen, int *na, int *ArrLen, long int *ArrOffset, int *Date, float *ut, int *Beam, 
				int *Channel, int *ScanCode, int *nGates, int *lagfr, int *smsep){
	int i;
	long int p;
	int magic, size, ns;
	p=0;
	for (i=0;i<nRec;i++) {
		fseek(F,p,SEEK_SET);
		ReadRecordHeader(F,&magic,&size,&ns,&na[i]);
		ReadRecordScalars(F,ns,&Date[i],&ut[i],&Beam[i],&Channel[i],&ScanCode[i],&nGates[i],&lagfr[i],&smsep[i]);
		ArrOffset[i] = ftell(F);
		ArrLen[i] = GetArrayLen(F,ArrOffset[i],na[i]);
		RecLen[i] = size;
		p += size;
	}
}

void GetArrays(FILE *F, int nRec, int *na, int *ArrLen, long int *ArrOffset, int *rDate, float *rut, int *rBeam, 
				int *rChannel, int *rScanCode, int *rnGates, int *rlagfr, int *rsmsep, int *Date, float *ut, int *Beam, 
				int *Channel, int *ScanCode, int *nGates, int *lagfr, int *smsep, float *V, float *P_l, float *W_l, int *Gnd, int *Gate) {
	int i, j;
	long int p = 0;		
	for (i=0;i<nRec;i++) {
		if (ArrLen[i] > 0) {
			for (j=0;j<ArrLen[i];j++) {
				Date[p+j] = rDate[i];
				ut[p+j] = rut[i];
				Beam[p+j] = rBeam[i];
				Channel[p+j] = rChannel[i];
				ScanCode[p+j] = rScanCode[i];
				nGates[p+j] = rnGates[i];
				lagfr[p+j] = rlagfr[i];
				smsep[p+j] = rsmsep[i];
			}
			ReadRecordArrays(F,ArrOffset[i],p,na[i],ArrLen[i],V,P_l,W_l,Gnd,Gate);
			p+=ArrLen[i];
		} else {
			Date[p] = rDate[i];
			ut[p] = rut[i];
			Beam[p] = rBeam[i];
			Channel[p] = rChannel[i];
			ScanCode[p] = rScanCode[i];
			nGates[p] = rnGates[i];
			lagfr[p] = rlagfr[i];
			smsep[p] = rsmsep[i];
			V[p] = 	NAN;
			P_l[p] = NAN;
			W_l[p] = NAN;
			Gnd[p] = 0;
			Gate[p] = -1;		
			p++;
		}
	}		
}


void ReadFITACF(const char *FileName, int *nRec, int *n, int **oDate, float **out, int **oBeam, 
				int **oChannel, int **oScanCode, int **onGates, int **olagfr, int **osmsep, 
				float **oV, float **oP_l, float **oW_l, int **oGnd, int **oGate, int Verbose) {
	
	if (Verbose ==1) {
		printf("Reading File: %s",FileName);
	}
	long int FLen, FPos;
	FILE *F;
	F = fopen(FileName,"r");
	FLen = FileSize(F);
	if (Verbose ==1) {
		printf(", File Size: %ld bytes",FLen);
	}
	*nRec = CountRecords(F,FLen);
	if (Verbose ==1) {
		printf(", Records: %d...",*nRec);
	}
	int rDate[*nRec],rBeam[*nRec],rChannel[*nRec],rScanCode[*nRec],rnGates[*nRec],rlagfr[*nRec],rsmsep[*nRec],ArrLen[*nRec],RecLen[*nRec],na[*nRec];
	float rut[*nRec];
	long int ArrOffset[*nRec];
	GetScalars(F,*nRec,RecLen,na,ArrLen,ArrOffset,rDate,rut,rBeam,rChannel,rScanCode,rnGates,rlagfr,rsmsep);
	int i;
	*n = 0;
	for (i=0;i<*nRec;i++) {
		if (ArrLen[i] == 0) {
			(*n)++;
		} else {
			(*n) += ArrLen[i];
		}
	}
	int *Date,*Beam,*Channel,*ScanCode,*nGates,*lagfr,*smsep,*Gnd,*Gate;
	float *ut,*V,*P_l,*W_l;	
	Date = (int*) malloc((*n)*sizeof(int));
	ut = (float*) malloc((*n)*sizeof(float));
	Beam = (int*) malloc((*n)*sizeof(int));
	Channel = (int*) malloc((*n)*sizeof(int));
	ScanCode = (int*) malloc((*n)*sizeof(int));
	nGates = (int*) malloc((*n)*sizeof(int));
	lagfr = (int*) malloc((*n)*sizeof(int));
	smsep = (int*) malloc((*n)*sizeof(int));
	V = (float*) malloc((*n)*sizeof(float));
	P_l = (float*) malloc((*n)*sizeof(float));
	W_l = (float*) malloc((*n)*sizeof(float));
	Gnd = (int*) malloc((*n)*sizeof(int));
	Gate = (int*) malloc((*n)*sizeof(int));
	GetArrays(F,*nRec,na,ArrLen,ArrOffset,rDate,rut,rBeam,rChannel,rScanCode,rnGates,rlagfr,
				rsmsep,Date,ut,Beam,Channel,ScanCode,nGates,lagfr,smsep,V,P_l,W_l,Gnd,Gate);
	fclose(F);
	
	*oDate = Date;
	*out = ut;
	*oBeam = Beam;
	*oChannel = Channel;
	*oScanCode = ScanCode;
	*onGates = nGates;
	*olagfr = lagfr;
	*osmsep = smsep;
	*oV = V;
	*oP_l = P_l;
	*oW_l = W_l;
	*oGnd = Gnd;
	*oGate = Gate;
	
	if (Verbose ==1) {
		printf("Done\n");
	}
	
}

void FreeInt(int *ptr) {
	free(ptr);
}

void FreeFloat(float *ptr) {
	free(ptr);
}
