import java.util.*;
import java.io.*;

class Lf{

    public static void main(String args[])throws IOException
    {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter production ");
        String n = br.readLine();
        String[] prods = n.split("=")[1].split("/");
        char[] prod1 = prods[0].toCharArray();
        char[] prod2 = prods[1].toCharArray();
        char nt = n.charAt(0);
        int l = 0;
        for(int i =0 ; i < prod1.length || i<prod2.length; i ++)
        {
            if(prod1[i]==prod2[i])
            {
                l++;
            }
            else{
                break;
            }
        }
        String factor = new String(prod1).substring(0,l);
        String remaining = new String(prod1).substring(l) + "/"+ new String(prod2).substring(l);
        System.out.println(nt+"="+factor+nt+"'");
        System.out.println(nt+"'="+remaining);

    }
}