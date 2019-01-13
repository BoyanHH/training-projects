
public class strawberries {
    public static void main(String[] args){
        int K=100 ;// reda
        int L=100;//stulba
        int R=60;// dni
        int currentDay=0;
        int[][] strawberries= new int[K][L];
        int badL=0;
        int badK=99;
       int badL2=49;
       int badK2=50;
              
        for(int i=0;i<K;i++){
            for(int j=0;j<L;j++){
                strawberries[i][j]=0;
            }
        }
          strawberries[badK][badL]=1;
         strawberries[badK2][badL2]=1;
                ///printira matricata
                System.out.println("Day: "+currentDay);
for (int i = 0; i < strawberries.length; i++) {
    for (int j = 0; j < strawberries[i].length; j++) {
        System.out.print(strawberries[i][j] + " ");
    }
    System.out.println();
        }


    int[][] temp=new int[K][L];
for(int i=0;i<K;i++){
            for(int j=0;j<L;j++){
                temp[i][j]=strawberries[i][j];
            }
        }         


boolean changed=false;

while(R>currentDay){
 for(int z=0;z<K;z++){
            for(int j=0;j<L;j++){              
                if(temp[z][j]==1){
                    System.out.println(temp[z][j]+" for "+z+" "+j);
              

                   if(z==0&&j==L-1){
                       System.out.println("a");
                     strawberries[z+1][j]=1;
                    // strawberries[z-1][j]=1;
                    // strawberries[z][j+1]=1;
                     strawberries[z][j-1]=1;
                     changed=true;
                   }
                   else if(z==K-1&&j==K-1){
                    //  strawberries[z+1][j]=1;
                     strawberries[z-1][j]=1;
                  //   strawberries[z][j+1]=1;
                     strawberries[z][j-1]=1;
                   }
                   else if(z==0&&j==0){
                          strawberries[z+1][j]=1;
                  //   strawberries[z-1][j]=1;
                     strawberries[z][j+1]=1;
                 //    strawberries[z][j-1]=1;
                   }
               else    if(z==K-1&&j==L-L){
                       strawberries[z-1][j]=1;
                     strawberries[z][j+1]=1; 
                     changed=true;
                   }
                   else if(z==0){
                       strawberries[z+1][j]=1;
                     //strawberries[z-1][j]=1;
                     strawberries[z][j+1]=1;
                     strawberries[z][j-1]=1;
                   }
                   else if(j==0){
                       strawberries[z+1][j]=1;
                     strawberries[z-1][j]=1;
                     strawberries[z][j+1]=1;
                    // strawberries[z][j-1]=1;
                   }
                   else if(z==K-1){
                       
                       // strawberries[z+1][j]=1;
                     strawberries[z-1][j]=1;
                     strawberries[z][j+1]=1;
                     strawberries[z][j-1]=1;
                   }
                   else if(j==K-1){
                    System.out.println("c");
                     strawberries[z+1][j]=1;
                     strawberries[z-1][j]=1;
                   //  strawberries[z][j+1]=1;
                     strawberries[z][j-1]=1;
                   }                  
                   else{
                                              System.out.println("b");
                          strawberries[z+1][j]=1;
                     strawberries[z-1][j]=1;
                     strawberries[z][j+1]=1;
                     strawberries[z][j-1]=1;
                   }
                  

             }
                }
 }

                    
             currentDay++;
               System.out.println("Day: "+currentDay);
for (int i = 0; i < strawberries.length; i++) {
    for (int j = 0; j < strawberries[i].length; j++) {
        System.out.print(strawberries[i][j] + " ");
    }
        System.out.println();
}
//populvame temp nanovo
for(int i=0;i<K;i++){
            for(int j=0;j<L;j++){
                temp[i][j]=strawberries[i][j];
            }
        }      
         
//broim loshite borovinki
int broiZdraviQgodi=0;
    for(int i=0;i<K;i++){
            for(int j=0;j<L;j++){
                if(strawberries[i][j]==0){
                    broiZdraviQgodi++;
                }
            }
        }
    System.out.println("Broi zdravi qgodi: "+broiZdraviQgodi);
}
    }
}



