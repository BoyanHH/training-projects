//rebro pri 2 obshti tochki1
package javapik3;

import java.util.Scanner;

public class round {
    static int countThings=0;
    static boolean checker = true;
    
    static int needThis =0;
    public static void main(String[] args){
        System.out.println("hi");
        Scanner sc = new Scanner(System.in);
        int n=0;
        while(2>n && n<1000){
           // n = sc.nextInt();
           n=9;
        }
        needThis=n;
    int[][] CA = new int[n][3];
        int[][] rebra = new int[n][n];

            //da ime Scanner koito da gi priema, za testovi celi direktno zadavam chislata
            CA[0][0]=0;
            CA[0][1]=0;
            CA[0][2]=2;
            CA[1][0]=3;
            CA[1][1]=0;
            CA[1][2]=2;
            CA[2][0]=6;
            CA[2][1]=0;
           CA[2][2]=2;    
            CA[3][0]=-7;
            CA[3][1]=6;
            CA[3][2]=5;  
             CA[4][0]=4;
            CA[4][1]=6;
            CA[4][2]=2;
            CA[5][0]=8;
            CA[5][1]=7;
            CA[5][2]=5;
            CA[6][0]=9;
            CA[6][1]=0;
           CA[6][2]=8;    
            CA[7][0]=19;
            CA[7][1]=8;
            CA[7][2]=7;            
             CA[8][0]=25;
            CA[8][1]=4;
            CA[8][2]=2;
           
            
            
                    //dokosvat se   
                    //k1k2
                    int i=0;
                    int j=i+1;
                    boolean Touch=false;
                   while(n>i-1){
                       j=i+1;
                       while(n>j){
                           System.out.print("j is "+j);
                       System.out.println("Checking: Circle"+i+" Circle "+(j));
                       double s1 = Math.sqrt(((CA[i][0]-CA[j][0])+(CA[i][1]-CA[j][1]))*((CA[i][0]-CA[j][0])+(CA[i][1]-CA[j][1])));
                       System.out.println("s is "+s1);
                       if(s1<CA[i][2]+CA[j][2]){
                       System.out.println("circle:"+i+(j)+" touch twice");          
                       Touch=true;
                   }
                       if(Touch==true){//ima rebro
                       rebra[i][j]=1;
                           
                       }
                           else{
                           System.out.println("no");
                       }
                                    j++;
                       }
                                              i++;

                   }
                                       
                                            i=n-1;
                         while(i>0){
                       boolean a =checkIfTouch(rebra,n-1,i);
       System.out.println("counter:"+countThings);
                       System.out.println("end");
                       i--;
                      countThings=0;

                         }                   
                   //rekursiq
    }
    public static boolean checkIfTouch(int[][] rebra, int c1, int c2){
       
        while(c2>0){
              System.out.println(checkIfTouch(rebra,c2,c2-1));

            if(rebra[c1][c2]==1||rebra[c2][c1]==1){                
                countThings++;
             //   System.out.println("here0");
              boolean c = checkIfTouch(rebra,c2,c2-1); 
              if(c==false){
                  break;
              }
                checker = true;
        }
            else{
                                              countThings=0;

                //nevaliden, ako e predi here0, to nqma nikakuv put
                checker = checkIfTouch(rebra,c2,c2-1);
                if(checker==false){
                System.out.println("THIS ROUTE IS -1");
                return checker;
                }
            }
                        c2--;

        }       
        
       System.out.println("counter:"+countThings);
        return false;
    }
}
