import java.util.*;
import java.io.*;

class Lr{

    public static void main(String args[])throws IOException
    {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter number of productions ");
        int n = Integer.parseInt(br.readLine());
        int index;
        System.out.println("Enter productions");
        for(int i = 0; i < n;i++)
        {
            String s= br.readLine();
            char nt = s.charAt(0);
            char[] ss = s.substring(2).toCharArray();
            for(int j =0 ; j<ss.length;j++)
            {
                if(nt == ss[j])
                {
                    System.out.println("Left Recursion");
                    char alpha = ss[j+1];
                    index = j;
                    while (ss[index]!='/')
                    index++;
                    char beta = ss[index+1];
                    System.out.println(nt+"="+beta+nt+"'");
                    System.out.println(nt+"'="+alpha+nt+"'"+"/E");
              }
            }
        }
    }
}
