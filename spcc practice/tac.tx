import java.util.*;
import java.io.*;

class Main{

    public static void main(String args[])
    {
        Scanner sc= new Scanner(System.in);
        System.out.println("Enter string");
        String input = sc.nextLine();
        String[] input_split = input.split("=");
        char[] input_char = input_split[1].toCharArray();
        char[][] t = new char[3][3];
        int count = 0;
        String t_val = new String();
        for(int i =0; i< input_char.length;i++)
        {
            if(input_char[i]=='/'||input_char[i]=='*'||input_char[i]=='%')
            {
                t[count][0] = input_char[i-1];
                t[count][1] = input_char[i];
                t[count][2] = input_char[i+1];
                count++;
            }
            if(input_char[i]=='+'||input_char[i]=='-')
            {
                t[2][0] = '1';
                t[2][1] = input_char[i];
                t[2][2] = '2';
            }
        }
        for(int i = 0; i<3;i++)
        {
            if(i==0)
            {
                t_val = "t1";
            }else if(i==1){
                t_val="t2";
            }else{
                t_val = "t3";
            }
            System.out.println("\n"+t_val+"=");
            for(int j=0 ; j<3;j++)
            {
                if(i==2){
                    if(j==0 || j==2)
                    {
                        System.out.println("t"+t[i][j]);
                    }
                    else{
                        System.out.println(t[i][j]);
                    }
                }
                else{
                    System.out.println(t[i][j]);
                }
            }
        }
    }
}