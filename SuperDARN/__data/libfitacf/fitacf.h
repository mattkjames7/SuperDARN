#ifndef __FITACF_H__
#define __FITACF_H__
#define _USE_MATH_DEFINES
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <cstring>
#endif
using namespace std;

typedef struct	{
	int Date;
	int Beam;
	int Channel;
	int ScanCode;
	int nGates;
	int smsep;	
	int lagfr;
	int ArrLen;			/* the number of array elements */
	int RecLen;			/* The length of the record in bytes */
	int na;				/* the number of array variables */
	float ut;
	long int ArrOffset;	/* file offset where the arrays start */
} scalars;

typedef struct {
	int Date;
	float ut;
	int Beam;
	int Channel;
	int ScanCode;
	int nGates;
	int lagfr;
	int smsep;
	float V;
	float P_l;
	float W_l;
	int Gnd;
	int Gate;
} arrays;

class fitacf {
	
	public:
		/* constructors/destructors */
		fitacf(const char*,bool);
		~fitacf();
		
		/* member functions to retrieve parameters */
		int GetScalarLen();
		void GetScalars(int *Date, float *ut, int *Beam, int *Channel,
						int *ScanCode, int *nGates, int *smsep, 
						int *lagfr, int *ArrLen, int *RecLen, int *na, 
						long int *ArrOffset);
		int GetArrayLen();
		void GetArrays(	int *Date, float *ut, int *Beam, int *Channel,
						int *ScanCode, int *nGates, int *smsep, 
						int *lagfr, float *V, float *P_l, float *W_l,
						int *Gnd, int *Gate);

	private:
		/* file pointer */
		FILE *F_;
		
		/* this will tell us whether the file exists and whether 
		 * the data was successfully read */
		bool fileExists_;
		
		/* the size of the file in bytes */
		long int FLen_;
		
		/* the number of records in the file */
		int nRec_;
		
		/* pointers to data stored in each record (these are the scalars
		 * from each record - i.e. one per record)*/
		bool allocScalars_;
		scalars *scalars_;
		
		/* total number of elements in all arrays combined */
		int n_;
		
		/* pointers to arrays */
		bool allocArrays_;
		arrays *arrays_;
		
		/* get the file size */
		void _FileSize();

		/* Get the number of records from the file */
		void _CountRecords();

		/* read a string */
		void _ReadString(char *str, int *len);

		/* read the header of a record */
		void _ReadRecordHeader(int *magic, int *size, int *ns, int *na);

		/* read in the scalars */
		void _ReadRecordScalars(int ns, int I);
		void _ReadAllScalars();
		
		/* read in the arrays */
		void _ReadRecordArrays(int I, int pos);
		int _GetArrayLen(long int FileOffset, int na);
		void _GetTotalArrayLen();
		void _ReadAllArrays();		

};
