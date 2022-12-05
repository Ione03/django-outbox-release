from django import template
register=template.Library()
@register.filter
def phone_number(number):
	B='-';A=number;G=['62','60','65','63','66','84']
	if A[:2]in G:C=A[:2];D=A[2:4];E=A[4:7];F=A[7:10];H=A[10:];return'('+C+')'+' '+D+B+E+B+F+B+H
	elif A:C=A[:3];D=A[3:6];E=A[6:9];F=A[9:];return'('+C+')'+' '+D+B+E+B+F
	return''
@register.filter
def replace_with(string,find_replace=',|_'):A=find_replace;print(A);B,C=A.split('|');print('[',B,C,']');return string.replace(B,C)