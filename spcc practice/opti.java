import java.util.*;
class opti{
    public static void main(String args[])
    {
        Scanner sc = new Scanner(System.in);
        System.out.println("enter no. of productions");
        int n = sc.nextInt();
        sc.nextLine();
        LinkedHashMap <String,Integer> hsh = new LinkedHashMap<String,Integer>();
        int cnt = 1;
         System.out.println("Enter production rules");
         for(int i = 0; i<n ; i++)
         {
             String r = sc.nextLine();
             int I = r.indexOf("=");
             String c = r.substring(I+1);
             if(hsh.containsKey(c))
             continue;
             else{
                 hsh.put(c,cnt);
                 cnt++;
             }
         }
         System.out.println("Optimized Code");
         for(Map.Entry<String,Integer>it:hsh.entrySet())
         {
             System.out.println("t"+it.getValue()+"="+it.getKey());
         }
    }
}